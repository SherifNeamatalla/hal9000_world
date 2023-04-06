import json
import os.path
from pathlib import Path

import openai
import yaml

from agents.memory.file_long_term_memory import FileLongTermMemory
from agents.memory.short_term_memory import BaseMemory
from commands.commands_executor import execute_cmd
from display.cmd_line_display import CmdLineDisplay
from logger.logger import log
from prompts.prompt_loader import load_commands_set, load_prompt
from util import token_counter

CONSTRAINTS_RESOURCES_PROMPT_NAME = "constraints_resources_prompt.txt"
RESPONSE_FORMAT_PROMPT_NAME = "response_format_prompt.txt"
BASE_COMMANDS_SET_NAME = "base_commands_prompt.txt"

USER_ROLE = "user"
SYSTEM_ROLE = "system"
ASSISTANT_ROLE = "assistant"

MODELS_DIR = os.path.join(Path(__file__).parent.parent, "storage", "agents")

ACTION_DENIED = "Action denied"

BASE_AGENT_TYPE = "BaseAgent"
JSON_LOADING_ERROR = "Loading response JSON"

MEMORY_COMMAND = "memory"
USER_COMMAND = "user"


class BaseAgent:
    def __init__(self, name, role, config, goals=[], display_manager=CmdLineDisplay(), voice_manager=None):
        # This holds the long term memory, agent decides what to store here
        self.name = name
        self.role = role
        self.goals = goals
        self.personal_goals = []
        # TODO: Should be able to load this from a config and a factory
        self.long_term_memory = FileLongTermMemory(self.name)
        # This holds the current conversation
        self.short_term_memory = BaseMemory(self.name)
        self.display_manager = display_manager
        self.voice_manager = voice_manager
        # This is the prompt that that we use to initialize the agent
        self.hello_world = None
        self.config = config
        self.init_wakeup_prompt(self.config.get('commands_set_path'))
        self.save()

    def wake(self):
        log(f"Agent {self.name} is waking up")
        # Adds a pseudo user prompt to make the agent start the conversation
        return self.chat(self.config.get('default_user_input'))

    def chat(self, user_input=None):
        # Can happen after user prompt that last message is from user, use that instead of default if no user input
        # is given, but always add the default prompt as this will keep reminding the agent to stick to the format etc
        if not user_input:
            # If last message was a user don't add another one
            last_message = self.short_term_memory.get_last_message()
            if last_message and last_message['role'] == USER_ROLE:
                user_input = last_message['content'] + " and " + self.config.get('default_user_input')
            else:
                user_input = user_input + self.config.get('default_user_input') if user_input else self.config.get(
                    'default_user_input')

        context, remaining_tokens = self.create_context(user_input)

        log(f"Agent {self.name} is chatting with user input: {user_input}")

        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=context,
            temperature=self.config.get('temperature'),
            max_tokens=remaining_tokens,
        )

        new_response_json = response.choices[0].message["content"]

        log(f"Agent {self.name} got response: {new_response_json}")
        # Update short term memory
        self.short_term_memory.add(self.create_message(USER_ROLE, user_input))
        self.short_term_memory.add(self.create_message(ASSISTANT_ROLE, new_response_json))

        return new_response_json

    def act(self):
        # Find the last message from the assistant to act upon it
        response_json = self.short_term_memory.get_last_message(ASSISTANT_ROLE)

        try:
            response = json.loads(response_json)
        except json.JSONDecodeError as e:
            self.add_error_command(JSON_LOADING_ERROR, e)
            return

        # Has name and args
        command = response['command']

        thoughts = response['thoughts']

        log(f"Agent {self.name} is acting on command: {command} and thoughts: {thoughts}")

        self.write(thoughts)

        self.speak(thoughts)

        self.plan(thoughts)

        try:
            self.execute_command(command)
        except Exception as e:
            self.add_error_command(command['name'], e)

        # TODO use reasoning, plan, criticism

    def plan(self, thoughts):
        self.personal_goals = thoughts['plan'].split('\n')

        if len(self.personal_goals) > self.config.get('max_personal_goals'):
            self.personal_goals = self.personal_goals[:self.config.get('max_personal_goals')]

    def execute_command(self, command):
        if not command or not command['name']:
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

        can_continue = self.ask_for_permission(command)

        if not can_continue:
            return

        command_name = command['name']

        command_result = execute_cmd(command)

        log(f"Agent {self.name} executed command {command_name} and got result: {command_result}")

        self.add_command_result(command_name, command_result)

    def execute_user_prompt_command(self, command_args, command_type):
        if command_type == 'prompt':
            user_input = self.display_manager.prompt_user_input(command_args['prompt'])
            self.add_command_result(USER_COMMAND, user_input)

    def ask_for_permission(self, command):
        if not self.config.get('autonomous'):
            command_name, user_input = self.display_manager.ask_permission(self.name, command)

            if user_input == 'n':
                self.add_human_feedback(ACTION_DENIED)
                return False

            if command_name == "human_feedback":
                self.add_human_feedback(user_input)
                return False

        return True

    def execute_memory_command(self, command_args, command_type):
        if command_type == 'set':
            self.long_term_memory.set(command_args['key'], command_args['value'])
        elif command_type == 'delete':
            self.long_term_memory.delete(command_args['key'])
        elif command_type == 'get':
            result = self.long_term_memory.get(command_args['key'])
            self.add_command_result(MEMORY_COMMAND, result)

    def write(self, thoughts):
        if not self.display_manager:
            return

        self.display_manager.print_agent_message(self.name, thoughts['text'])

    def speak(self, thoughts):
        if not self.voice_manager:
            return

        self.voice_manager.speak(thoughts['speak'])

    def add_error_command(self, command_name, error):
        command_memory_entry = f"Command {command_name} failed, error:{str(error)}"

        self.short_term_memory.add(self.create_message(SYSTEM_ROLE, command_memory_entry))

    def add_command_result(self, command_name, command_result):
        if not command_result:
            command_memory_entry = f"Unable to execute command {command_name}"
        else:
            command_memory_entry = f"Command {command_name} returned: {command_result}"

        self.short_term_memory.add(self.create_message(SYSTEM_ROLE, command_memory_entry))

    def add_human_feedback(self, user_input):
        result = f"Human feedback: {user_input}"
        self.short_term_memory.add(self.create_message(SYSTEM_ROLE, result))

    def create_context(self, user_input):
        context = self.create_long_term_memory_context()

        short_term_result = self.create_short_term_memory_context(context, user_input)

        context = short_term_result[0]
        remaining_tokens = short_term_result[1]

        return context, remaining_tokens

    def create_long_term_memory_context(self):
        # Add the Who you are, your goals, constraints, resources and response format
        # Add the permanent memory of the agent
        return [self.create_message(SYSTEM_ROLE, self.hello_world),
                self.create_message(SYSTEM_ROLE, self.long_term_memory.get_as_string()),
                self.create_message(SYSTEM_ROLE, 'User Goals: ' + '\n'.join(self.goals)),
                self.create_message(SYSTEM_ROLE, 'Personal Goals: ' + '\n'.join(self.personal_goals))]

    def create_short_term_memory_context(self, context, user_input):
        # Add the short term memory of the agent, we will use token_counter ( Thank you Auto-GPT ! ) to add just the
        # right length of the short term memory, shouldn't exceed self.config.get('max_tokens')

        # Add the user input
        full_message_history = self.short_term_memory.get()
        model = self.config.get('model')
        token_limit = self.config.get('max_tokens') - token_counter.count_message_tokens(context, model)
        send_token_limit = token_limit - 1000
        next_message_to_add_index = len(full_message_history) - 1
        current_tokens_used = 0
        insertion_index = len(context)

        # Count the currently used tokens
        current_tokens_used = token_counter.count_message_tokens(context, model)
        current_tokens_used += token_counter.count_message_tokens([self.create_message(USER_ROLE, user_input)],
                                                                  model)  # Account for user input (appended later)

        while next_message_to_add_index >= 0:
            # print (f"CURRENT TOKENS USED: {current_tokens_used}")
            message_to_add = full_message_history[next_message_to_add_index]

            tokens_to_add = token_counter.count_message_tokens([message_to_add], model)
            if current_tokens_used + tokens_to_add > send_token_limit:
                break

            # Add the most recent message to the start of the current context, after the two system prompts.
            context.insert(insertion_index, full_message_history[next_message_to_add_index])

            # Count the currently used tokens
            current_tokens_used += tokens_to_add

            # Move to the next most recent message in the full message history
            next_message_to_add_index -= 1

        # Append user input, the length of this is accounted for above
        context.extend([self.create_message(USER_ROLE, user_input)])

        tokens_remaining = token_limit - current_tokens_used

        return context, tokens_remaining

    def init_wakeup_prompt(self, commands_set_path):
        new_prompt = f"You are {self.name}, {self.role}"
        if self.config.get('include_constraints_resources_prompt'):
            new_prompt += '\n' + load_prompt(CONSTRAINTS_RESOURCES_PROMPT_NAME)

        if self.config.get('include_response_format_prompt'):
            new_prompt += '\n' + load_prompt(RESPONSE_FORMAT_PROMPT_NAME)

        if self.config.get('include_commands_set') and self.config.get('commands_set_path'):
            new_prompt += '\n' + load_commands_set(commands_set_path)
        self.hello_world = new_prompt

    def save(self):
        if not self.config.get('save_model'):
            return
        agent_path = os.path.join(MODELS_DIR, self.name)
        # create new dir if not exists
        if not os.path.exists(MODELS_DIR):
            os.makedirs(MODELS_DIR)

        if not os.path.exists(agent_path):
            os.makedirs(agent_path)

        self.long_term_memory.save()

        with open(os.path.join(agent_path, 'config.yaml'), 'w') as outfile:
            yaml_content = {
                "name": self.name,
                "role": self.role,
                "model": self.config.get('model'),
                "config": self.config.to_dict(),
                "hello_world": self.hello_world,
            }
            yaml.dump(yaml_content, outfile, default_flow_style=False)

    @staticmethod
    def create_message(role, content):
        return {
            "role": role,
            "content": content
        }
