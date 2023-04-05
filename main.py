import os

import openai
from dotenv import load_dotenv

from agents.base_agent import BaseAgent, BASE_COMMANDS_SET_NAME
from display.cmd_line_display import CmdLineDisplay

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_user_input():
    return input("User Input: ")


def main():
    display = CmdLineDisplay()
    # Get user input to initialize the agent
    name = input("Enter the name of the agent: ")
    role = input("Enter the role of the agent: ")
    commands_set_path = input("Enter the path to the commands set file (or press enter for default): ")
    if commands_set_path == "":
        commands_set_path = BASE_COMMANDS_SET_NAME

    # Initialize the agent
    agent = BaseAgent(name=name, role=role, commands_set_path=commands_set_path)

    agent_hello_world = agent.wake()

    display.print_agent_message(agent.name, agent_hello_world)
    # Enter an infinite loop that prompts the user for input and sends it to the agent for processing
    while True:
        user_input = get_user_input()
        response = agent.chat(user_input)
        agent.act(response)


if __name__ == "__main__":
    main()
