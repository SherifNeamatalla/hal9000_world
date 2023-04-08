import json5 as json
import openai

from agents.memory.file_long_term_memory import FileLongTermMemory
from agents.memory.short_term_memory import BaseMemory
from commands.commands_executor import execute_cmd
from config.app_config import AppConfig
from config.constants import *
from logger.logger import log
from prompts.prompt_loader import load_commands_set, load_prompt
from util.token_counter import create_short_term_memory_context
from util.util import create_message


class BaseAgent:
    def __init__(self, name, role, config, agent_id=None, goals=[], personal_goals=[], long_term_memory="",
                 short_term_memory=""):
        # This holds the long term memory, agent decides what to store here
        self.id = agent_id
        self.name = name
        self.role = role
        self.goals = goals
        self.personal_goals = personal_goals
        # TODO: Should be able to load this from a config and a factory
        self.long_term_memory = FileLongTermMemory(self.name, long_term_memory)
        # This holds the current conversation
        self.short_term_memory = BaseMemory(self.name, short_term_memory)
        self.config = config

    def wake(self):
        log(f"Agent {self.name} is waking up...")
        # Adds a pseudo user prompt to make the agent start the conversation
        return self.chat(self.config.get('default_user_input'))

    def chat(self, user_input=None):
        original_user_input = user_input
        # Can happen after user prompt that last message is from user, use that instead of default if no user input
        # is given, but always add the default prompt as this will keep reminding the agent to stick to the format etc
        if not user_input:
            # If last message was a user don't add another one
            last_message = self.short_term_memory.get_last_message()
            if last_message and last_message['role'] == USER_ROLE:
                self.short_term_memory.delete_last_message()
                user_input = last_message['content'] + ", " + self.config.get('default_user_input')

            else:
                user_input = self.config.get('default_user_input')

        elif not user_input == self.config.get('default_user_input'):
            user_input = user_input + ", " + self.config.get('default_user_input')

        context, remaining_tokens = self.create_context(user_input)

        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=context,
            temperature=self.config.get('temperature'),
            max_tokens=remaining_tokens,
        )

        new_response_json = response.choices[0].message["content"]

        # Update short term memory
        # Using original to not include the system messages / inner user prompts in history
        if original_user_input:
            self.short_term_memory.add(create_message(USER_ROLE, original_user_input))
        self.short_term_memory.add(create_message(ASSISTANT_ROLE, new_response_json))

        return new_response_json

    def think(self):
        try:
            response_json = self.short_term_memory.get_last_message(ASSISTANT_ROLE)
            response = json.loads(response_json)
        except Exception as e:
            # This error will be shown to agent, maybe agent can react to it
            self.add_error_command(JSON_LOADING_ERROR, e)
            # Return error message, agent will also see this in its short term memory when it acts
            return None

        thoughts = response['thoughts']

        self.write(thoughts)

        self.speak(thoughts)

        self.plan(thoughts)

        return response['command']

    def act(self, command, user_input):
        command_name = command['name'] if command and command['name'] else None

        if user_input == WRONG_COMMAND:
            self.add_error_command(command_name, WRONG_COMMAND)

        # Action denied from user or not accepted, meaning human feedback
        if user_input == PERMISSION_DENIED or not user_input == PERMISSION_GRANTED:
            self.add_human_feedback(user_input)
            return user_input

        # Memory is handled by agent itself and not by the command executor
        if command_name == MEMORY_COMMAND:
            command_args = command.get('args', {})
            command_type = command.get('type', None)
            return self.execute_memory_command(command_args, command_type)

        try:
            return self.execute_command(command)
        except Exception as e:
            self.add_error_command(command['name'], e)
            return f"Error executing command {command['name'] if command and command['name'] else 'None'}"

    def plan(self, thoughts):
        self.personal_goals = thoughts['plan'].split('\n')

        if len(self.personal_goals) > self.config.get('max_personal_goals'):
            self.personal_goals = self.personal_goals[:self.config.get('max_personal_goals')]

        AppConfig().display_manager.print_agent_goals(self.goals, self.personal_goals)

    def write(self, thoughts):
        AppConfig().display_manager.print_agent_thoughts(thoughts['text'])

        AppConfig().display_manager.print_agent_criticism(thoughts['criticism'])

        AppConfig().display_manager.print_agent_reasoning(thoughts['reasoning'])

    def speak(self, thoughts):
        if not AppConfig().voice_manager:
            return

        AppConfig().voice_manager.speak(thoughts['speak'])

    def execute_command(self, command):
        command_name = command['name']

        AppConfig().display_manager.print_executing_command(command_name, command.get('args', {}),
                                                            command.get('type', None))

        command_result = execute_cmd(command)

        AppConfig().display_manager.print_command_result(command_name, command_result)

        self.add_command_result(command_name, command_result)

        return command_result

    def execute_memory_command(self, command_args, command_type):
        AppConfig().display_manager.print_executing_command(MEMORY_COMMAND, command_args, command_type)
        command_result = None
        if command_type == 'set':
            command_result = self.long_term_memory.set(command_args['key'], command_args['value'])
        elif command_type == 'delete':
            command_result = self.long_term_memory.delete(command_args['key'])
        elif command_type == 'get':
            command_result = self.long_term_memory.get(command_args['key'])
            self.add_command_result(MEMORY_COMMAND, command_result)

        AppConfig().display_manager.print_command_result(MEMORY_COMMAND, command_result)

        return command_result

    def add_error_command(self, command_name, error):
        command_memory_entry = f"Command {command_name} failed, error:{str(error)}"

        self.short_term_memory.add(create_message(SYSTEM_ROLE, command_memory_entry))

        AppConfig().display_manager.print_error(command_memory_entry)

    def add_command_result(self, command_name, command_result='None'):
        if not command_result:
            command_memory_entry = f"Unable to execute command {command_name}"
        else:
            command_memory_entry = f"Command {command_name} returned: {command_result}, save important information in " \
                                   f"memory!"

        self.short_term_memory.add(create_message(SYSTEM_ROLE, command_memory_entry))

    def add_human_feedback(self, user_input):
        result = f"Human feedback: {user_input}"
        self.short_term_memory.add(create_message(USER_ROLE, result))

    def create_context(self, user_input):
        context = self.create_long_term_memory_context()

        short_term_result = create_short_term_memory_context(self.config.get('model'),
                                                             self.config.get('max_tokens'), context, user_input,
                                                             self.short_term_memory.get())

        context = short_term_result[0]
        remaining_tokens = short_term_result[1]

        return context, remaining_tokens

    def create_long_term_memory_context(self):
        # Add the Who you are, your goals, constraints, resources and response format
        # Add the permanent memory of the agent
        user_goals = 'User Goals: ' + '\n' + '\n'.join(self.goals)
        personal_goals = 'Personal Goals: ' + '\n' + '\n'.join(self.personal_goals) if self.personal_goals and len(
            self.personal_goals) > 0 else ''

        message = self.hello_world(self.config.get('commands_set_path'), user_goals_str=user_goals,
                                   personal_goals_str="")

        return [create_message(SYSTEM_ROLE, message),
                create_message(SYSTEM_ROLE, self.long_term_memory.get_as_string())]

    def hello_world(self, commands_set_path, user_goals_str, personal_goals_str):
        prompt_start = load_prompt(self.config.get('prompt_start_path'))
        new_prompt = f"You are {self.name}, {self.role}\n{prompt_start}\n\n"

        if user_goals_str:
            new_prompt += "\n" + user_goals_str + "\n"

        if personal_goals_str:
            new_prompt += "\n" + personal_goals_str + "\n"

        if self.config.get('include_commands_set') and self.config.get('commands_set_path'):
            new_prompt += '\n' + load_commands_set(commands_set_path) + '\n'

        if self.config.get('include_constraints_resources_prompt'):
            new_prompt += '\n' + load_prompt(CONSTRAINTS_RESOURCES_PROMPT_NAME) + '\n'

        if self.config.get('include_response_format_prompt'):
            new_prompt += '\n' + load_prompt(RESPONSE_FORMAT_PROMPT_NAME)

        return new_prompt

    def save(self):
        if not self.config.get('save_model'):
            return

        AppConfig().save(self)

    def display(self):
        if not AppConfig().display_manager:
            return

        AppConfig().display_manager.print_agent_goals(self.goals, self.personal_goals)

    def get_filtered_short_term_memory(self):
        memory = self.short_term_memory.memory
        filtered_memory = []
        # Remove all user prompts that = default user prompt
        for entry in memory:
            if entry['role'] != USER_ROLE or entry['content'] != self.config.get('default_user_input'):
                filtered_memory.append(entry)

        return filtered_memory

    @staticmethod
    def load_from_dict(data):
        from agents.config import AgentConfig
        name = data.get('name')
        role = data.get('role')
        goals = data.get('goals')
        long_term_memory = data.get('long_term_memory')
        short_term_memory = data.get('short_term_memory')
        config = AgentConfig.from_dict(data.get('config'))

        # TODO support other types,or now just BaseAgent
        return BaseAgent(name, role, config, goals=goals, personal_goals=[], long_term_memory=long_term_memory,
                         short_term_memory=short_term_memory)
