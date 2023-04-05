import os
from pathlib import Path

from logger.logger import log

PROMPTS_DIR = Path(__file__).parent
COMMANDS_SETS_DIR = "commands_sets"


def load_commands_set(commands_set_file_name):
    try:
        # get directory of this file:
        command_path = os.path.join(PROMPTS_DIR, COMMANDS_SETS_DIR, commands_set_file_name)
        # Load the prompt from prompts/prompt.txt
        with open(command_path, "r") as prompt_file:
            prompt = prompt_file.read()

        return prompt
    except FileNotFoundError:
        log("Error: Prompt file not found")
        return ""


def load_prompt(prompt_file_name):
    try:
        # get directory of this file:
        command_path = os.path.join(PROMPTS_DIR, prompt_file_name)
        # Load the prompt from prompts/prompt.txt
        with open(command_path, "r") as prompt_file:
            prompt = prompt_file.read()

        return prompt
    except FileNotFoundError:
        log("Error: Prompt file not found")
        return ""
