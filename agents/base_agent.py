import os.path

import json5 as json
import openai
import yaml

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
    def __init__(self, name, role, config, goals=[], personal_goals=[]):
        # This holds the long term memory, agent decides what to store here
        self.name = name
        self.role = role
        self.goals = goals
        self.personal_goals = personal_goals
        # TODO: Should be able to load this from a config and a factory
        self.long_term_memory = FileLongTermMemory(self.name)
        # This holds the current conversation
        self.short_term_memory = BaseMemory(self.name)
        self.config = config
        self.save()

    def wake(self):
        log(f"Agent {self.name} is waking up...")
        # Adds a pseudo user prompt to make the agent start the conversation
        return self.chat(self.config.get('default_user_input'))

    def chat(self, user_input=None):
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
        else:
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
        self.short_term_memory.add(create_message(USER_ROLE, user_input))
        self.short_term_memory.add(create_message(ASSISTANT_ROLE, new_response_json))

        return new_response_json

    def act(self, response_json=None):
        if not response_json:
            # Find the last message from the assistant to act upon it
            response_json = self.short_term_memory.get_last_message(ASSISTANT_ROLE)

        try:
            response = json.loads(response_json)
        except Exception as e:
            # This error will be shown to agent, maybe agent can react to it
            self.add_error_command(JSON_LOADING_ERROR, e)
            return

        # Has name and args
        command = response['command']

        thoughts = response['thoughts']

        self.write(thoughts)

        self.speak(thoughts)

        self.plan(thoughts)

        try:
            self.execute_command(command)
        except Exception as e:
            self.add_error_command(command['name'], e)

        self.save()

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
        if not command or not command['name']:
            # When agent has no output command, this usually means they're going to an infinite loop
            self.ask_for_permission(command)
            return

        command_name = command['name']

        # If agent needs some user input to continue, ask for it
        if command_name == USER_COMMAND:
            command_args = command.get('args', {})
            command_type = command.get('type', None)
            self.execute_user_prompt_command(command_args, command_type)
            return

        # This hardcodes the agent to be able to automatically update its memory without user permission
        # to change this behaviour you can move this block after the autonomous check
        if command_name == MEMORY_COMMAND:
            # TODO: error if no command_args
            command_args = command.get('args', {})
            command_type = command.get('type', None)
            self.execute_memory_command(command_args, command_type)
            return

        can_continue = True
        if not command_name == SNOWFLAKE_COMMAND:
            can_continue = self.ask_for_permission(command)

        if not can_continue:
            return

        command_name = command['name']

        AppConfig().display_manager.print_executing_command(command_name, command.get('args', {}),
                                                            command.get('type', None))

        command_result = execute_cmd(command)

        AppConfig().display_manager.print_command_result(command_name, command_result)

        log(f"Agent {self.name} executed command {command_name} and got result: {command_result}")

        self.add_command_result(command_name, command_result)

        if command_name == SNOWFLAKE_COMMAND:
            user_input = AppConfig().display_manager.prompt_user_input(command_result)
            self.add_human_feedback(user_input)

    def execute_user_prompt_command(self, command_args, command_type):
        if command_type == 'prompt':
            user_input = AppConfig().display_manager.prompt_user_input(command_args['prompt'])
            self.add_human_feedback(user_input)

    def ask_for_permission(self, command):
        if not self.config.get('autonomous'):
            command_name, user_input = AppConfig().display_manager.ask_permission(self.name, command)

            if user_input == 'n':
                self.add_human_feedback(ACTION_DENIED)
                return False

            if command_name == "human_feedback":
                self.add_human_feedback(user_input)
                return False

        return True

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
        agent_path = os.path.join(AGENTS_DIR, self.name)
        # create new dir if not exists
        if not os.path.exists(AGENTS_DIR):
            os.makedirs(AGENTS_DIR)

        if not os.path.exists(agent_path):
            os.makedirs(agent_path)

        self.long_term_memory.save()

        with open(os.path.join(agent_path, 'config.yaml'), 'w') as outfile:
            yaml_content = {
                "name": self.name,
                "role": self.role,
                "model": self.config.get('model'),
                "config": self.config.to_dict(),
                "goals": self.goals,
                "personal_goals": self.personal_goals
            }
            yaml.dump(yaml_content, outfile, default_flow_style=False)

    def display(self):
        if not AppConfig().display_manager:
            return

        AppConfig().display_manager.print_agent_goals(self.goals, self.personal_goals)
