from agents.base_agent import BASE_COMMANDS_SET_NAME, BaseAgent
from agents.config import AgentConfig
from display.cmd_line_display import CmdLineDisplay
from runners.runner_interface import IRunner
from storage.storage_loader import load_agent


class AutoGptRunner(IRunner):
    def run(self):
        display = CmdLineDisplay()

        agent = self.load_agent(display)

        agent.wake()

        agent.act()
        while True:
            agent.chat()

            agent.act()

    def get_user_input(self):
        return input("User Input: ")

    @staticmethod
    def load_agent(display):
        load = display.prompt_user_input("Load agent? (y/n): ")

        if load == "y":
            name = display.prompt_user_input("Enter the name of the existing agent: ")

            agent = load_agent(agent_name=name)

        else:
            # Get user input to initialize the agent
            name = display.prompt_user_input("Enter the name of the agent: ")
            role = display.prompt_user_input("Enter the role of the agent: ")
            commands_set_path = display.prompt_user_input("Enter the path to the commands set: ")

            if commands_set_path == "":
                commands_set_path = BASE_COMMANDS_SET_NAME

            config = AgentConfig(commands_set_path=commands_set_path)

            # Initialize the agent
            agent = BaseAgent(name=name, role=role, config=config)

        return agent
