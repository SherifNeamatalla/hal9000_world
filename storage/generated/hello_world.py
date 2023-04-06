import os

import openai
from dotenv import load_dotenv

from agents.base_agent import BaseAgent, BASE_COMMANDS_SET_NAME
from agents.memory.file_long_term_memory import FileLongTermMemory
from commands.cmd_agents import CmdAgents, delete_agent, start_agent, list_agents
from display.cmd_line_display import CmdLineDisplay
from runners.auto_gpt_runner import AutoGptRunner
from util.storage_loader import load_agent

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_user_input():
    return input("User Input: ")


def main():
    # agent_cmd = CmdAgents()
    # delete_agent('TestAgent')
    # start_agent('TestAgent', 'Help me test my platform', 'You are an AI agent that helps me test my platform',
    #                       True)
    # list_agents()

    # memory = FileLongTermMemory("sensei")
    # memory.add("test")
    # agent = load_agent("sensei")
    #
    # agent.execute_command({
    #     "name": "memory",
    #     "type": "add",
    #     "args": {
    #         "value": "test2"
    #     }
    # })
    runner = AutoGptRunner()
    runner.run()


if __name__ == "__main__":
    main()
