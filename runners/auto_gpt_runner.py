from agents.base_agent import BASE_COMMANDS_SET_NAME, BaseAgent
from agents.config import AgentConfig
from config.app_config import AppConfig
from database.sqlite3_db_manager import SQLite3DBManager
from display.cmd_line_display import CmdLineDisplay
from display.spinner import Spinner
from runners.runner_interface import IRunner
from util.agents_util import load_agent_by_id
from util.commands_util import ask_user_command_permission


class AutoGptRunner(IRunner):
    def run(self):
        AppConfig(
            display_manager=CmdLineDisplay(),
            voice_manager=None,
            db_manager=SQLite3DBManager(),
            save_format='yaml'
        )

        agent = self.load_agent()

        with Spinner("Waking up... "):
            agent.wake()

        AppConfig().display_manager.print_hello_world(agent.name)
        agent.think()
        while True:
            with Spinner("Thinking... "):
                agent.chat()

            agent.think()

            suggested_command = agent.think()

            user_response = ask_user_command_permission(agent.name, suggested_command)

            agent.act(suggested_command, user_response)

            agent.save()

    @staticmethod
    def load_agent():
        load = AppConfig().display_manager.prompt_user_input("Load agent? (y/n): ")

        if load == "y":
            existing_agents = AppConfig().db_manager.list()

            # Show agents and get user input
            for i, agent in enumerate(existing_agents):
                print(f"{i}: {agent['name']}")

            agent_index = None

            while agent_index is None or not isinstance(agent_index, int) or int(agent_index) >= len(
                    existing_agents) or int(agent_index) < 0:
                try:
                    agent_index = int(AppConfig().display_manager.prompt_user_input(
                        "Enter a valid index for an existing agent: "))
                except ValueError:
                    agent_index = None

            agent_id = existing_agents[int(agent_index)]['id']

            agent = load_agent_by_id(agent_id)

        else:
            # Get user input to initialize the agent
            name = AppConfig().display_manager.prompt_user_input("Enter the name of the agent: ")

            role = AppConfig().display_manager.prompt_user_input("Enter the role of the agent: ")

            goals = []

            while True:
                goal = AppConfig().display_manager.prompt_user_input(
                    "Enter a goal for the agent (leave blank to finish): ")
                if goal == "":
                    break
                goals.append(goal)
            prompt_start_path = AppConfig().display_manager.prompt_user_input(
                "Enter the prompt start path: (Leave empty for default)")

            commands_set_path = AppConfig().display_manager.prompt_user_input("Enter the path to the commands set: ")

            if commands_set_path == "":
                commands_set_path = BASE_COMMANDS_SET_NAME

            if prompt_start_path == "":
                prompt_start_path = None

            config = AgentConfig(commands_set_path=commands_set_path, prompt_start_path=prompt_start_path)

            agent_id = AppConfig().db_manager.add(name, role, goals, config)

            # Initialize the agent
            agent = BaseAgent(agent_id=agent_id, name=name, role=role, config=config, goals=goals)

        return agent
