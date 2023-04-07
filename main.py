import os

import openai
from dotenv import load_dotenv

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
