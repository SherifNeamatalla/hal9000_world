import os

import openai
from dotenv import load_dotenv

from runners.auto_gpt_runner import AutoGptRunner

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
