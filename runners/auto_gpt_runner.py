from agents.base_agent import BASE_COMMANDS_SET_NAME, BaseAgent
from agents.config import AgentConfig
from display.cmd_line_display import CmdLineDisplay
from display.spinner import Spinner
from runners.runner_interface import IRunner
from util.storage_loader import load_agent


class AutoGptRunner(IRunner):
    def run(self):
        display = CmdLineDisplay()

        agent = self.load_agent(display)

        with Spinner("Waking up... "):
            agent.wake()

        display.print_hello_world(agent.name)
        agent.act()
        while True:
            with Spinner("Thinking... "):
                command_json = agent.chat()

            agent.act(command_json)

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
            prompt_start_path = display.prompt_user_input("Enter the prompt start path: (Leave empty for default)")

            commands_set_path = display.prompt_user_input("Enter the path to the commands set: ")

            if commands_set_path == "":
                commands_set_path = BASE_COMMANDS_SET_NAME

            if prompt_start_path == "":
                prompt_start_path = None

            goals = []

            while True:
                goal = display.prompt_user_input("Enter a goal for the agent (leave blank to finish): ")
                if goal == "":
                    break
                goals.append(goal)

            config = AgentConfig(commands_set_path=commands_set_path, prompt_start_path=prompt_start_path)

            # Initialize the agent
            agent = BaseAgent(name=name, role=role, config=config, goals=goals)

        return agent
