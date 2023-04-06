import os

import openai
from dotenv import load_dotenv

from agents.base_agent import BaseAgent, BASE_COMMANDS_SET_NAME
from display.cmd_line_display import CmdLineDisplay
from runners.auto_gpt_runner import AutoGptRunner

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_user_input():
    return input("User Input: ")


def main():
    runner = AutoGptRunner()
    runner.run()


if __name__ == "__main__":
    main()
