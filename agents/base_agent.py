import json
import os.path
from pathlib import Path

import openai
import yaml

from agents.config import AgentConfig
from agents.memory.file_long_term_memory import FileLongTermMemory
from agents.memory.short_term_memory import BaseMemory
from commands.commands_executor import execute_cmd
from display.cmd_line_display import CmdLineDisplay
from prompts.prompt_loader import load_commands_set, load_prompt
from util import token_counter

CONSTRAINTS_RESOURCES_PROMPT_NAME = "constraints_resources_prompt.txt"
RESPONSE_FORMAT_PROMPT_NAME = "response_format_prompt.txt"
BASE_COMMANDS_SET_NAME = "base_commands_prompt.txt"

USER_ROLE = "user"
SYSTEM_ROLE = "system"
ASSISTANT_ROLE = "assistant"

INITIAL_USER_INPUT = 'Determine which next command to use, and respond using the format specified above:'

MODELS_DIR = os.path.join(Path(__file__).parent.parent, "storage", "agents")

ACTION_DENIED = "Action denied"

BASE_AGENT_TYPE = "BaseAgent"


class BaseAgent:
    def __init__(self, name, role, config, display_manager=CmdLineDisplay(), voice_manager=None):
        # This holds the long term memory, agent decides what to store here
        self.name = name
        self.role = role
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
        # Adds a pseudo user prompt to make the agent start the conversation
        return self.chat(INITIAL_USER_INPUT)

    def chat(self, user_input=INITIAL_USER_INPUT):
        context, remaining_tokens = self.create_context(user_input)

        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=context,
            temperature=self.config.get('temperature'),
            max_tokens=remaining_tokens,
        )

        new_response_json = response.choices[0].message["content"]

        # Update short term memory
        self.short_term_memory.add(self.create_message(USER_ROLE, user_input))
        self.short_term_memory.add(self.create_message(ASSISTANT_ROLE, new_response_json))

        return new_response_json

    def act(self):
        # Find the last message from the assistant to act upon it
        response_json = self.short_term_memory.get_last_message(ASSISTANT_ROLE)

        response = json.loads(response_json)

        # Has name and args
        command = response['command']

        thoughts = response['thoughts']

        self.write(thoughts)

        self.speak(thoughts)

        self.execute_command(command)

        # TODO use reasoning, plan, criticism

    def execute_command(self, command):
        if not command or not command['name']:
            return

        command_name = command['name']

        # This hardcodes the agent to be able to automatically update its memory without user permission
        # to change this behaviour you can move this block after the autonomous check
        if command_name == 'memory':
            # TODO: error if no command_args
            command_args = command.get('command_args', {})
            command_type = command_args.get('type', None)
            self.execute_memory_command(command_name, command_args, command_type)
            return

        can_continue = self.ask_for_permission(command)

        if not can_continue:
            return

        command_name = command['name']

        command_result = execute_cmd(command)

        self.add_command_result(command_name, command_result)

        # Agent takes command feedback and updates its memory
        self.chat()

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

    def execute_memory_command(self, command_name, command_args, command_type):
        if command_type == 'overwrite':
            self.long_term_memory.set(command_args['key'], command_args['value'])
        elif command_type == 'delete':
            self.long_term_memory.delete(command_args['key'])
        elif command_type == 'add':
            self.long_term_memory.add(command_args['value'])

    def write(self, thoughts):
        if not self.display_manager:
            return

        self.display_manager.print_agent_message(self.name, thoughts['text'])

    def speak(self, thoughts):
        if not self.voice_manager:
            return

        self.voice_manager.speak(thoughts['speak'])

    def add_command_result(self, command_name, command_result):
        if not command_result:
            command_memory_entry = f"Unable to execute command {command_name}"
        else:
            command_memory_entry = f"Command {command_name} returned: {command_result}"

        self.short_term_memory.add(self.create_message(SYSTEM_ROLE, command_memory_entry));

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
                self.create_message(SYSTEM_ROLE, "Permanent memory: " + self.long_term_memory.get_as_string())]

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
