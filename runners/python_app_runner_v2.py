import json

from agents.base_agent import BASE_COMMANDS_SET_NAME, BaseAgent
from agents.config import AgentConfig
from agents.v2.agent import Agent
from agents.v2.agent_config_v2 import AgentConfigV2
from commands.commands_executor import execute_cmd
from config.app_config import AppConfig
from config.constants import WRONG_COMMAND, JSON_LOADING_ERROR, PERMISSION_DENIED, PERMISSION_GRANTED
from display.spinner import Spinner
from runners.runner_interface import IRunner
from util.agents_util import load_agent_by_id
from util.commands_util import ask_user_command_permission


def write(thoughts):
    AppConfig().display_manager.print_agent_thoughts(thoughts['text'])

    AppConfig().display_manager.print_agent_criticism(thoughts['criticism'])

    AppConfig().display_manager.print_agent_reasoning(thoughts['reasoning'])


def speak(thoughts):
    if not AppConfig().voice_manager:
        return

    AppConfig().voice_manager.speak(thoughts['speak'])


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

        config = AgentConfigV2()

        agent_id = AppConfig().db_manager.add(name, role, goals, config)

        # Initialize the agent
        agent = Agent(agent_id=agent_id, name=name, role=role, config=config, goals=goals)

    return agent


def plan(thoughts, goals):
    personal_goals = thoughts['plan'].split('\n')

    AppConfig().display_manager.print_agent_goals(goals, personal_goals)


def validate_last_response(agent):
    """Think about the generated response and see if it's correct"""
    """This method will be called by the runner as a part of the chat loop"""

    try:
        response_json = agent.memory.get_last_agent_message()
        response = json.loads(response_json)
        return response
    except Exception as e:
        # This error will be shown to agent, maybe agent can react to it
        agent.memory.add_error_command(JSON_LOADING_ERROR, e)
        AppConfig().display_manager.print_error(JSON_LOADING_ERROR)

        # Return error message, agent will also see this in its short term memory when it acts
        return None


def print_response(response, agent):
    suggested_command = response['command']

    thoughts = response['thoughts']

    write(thoughts)

    speak(thoughts)

    plan(thoughts, agent.goals)

    user_response = ask_user_command_permission(agent.name, suggested_command)

    return user_response, suggested_command


def execute_command(command, agent):
    command_name = command['name']
    command_args = command.get('args', [])
    command_type = command.get('type', 'command')
    AppConfig().display_manager.print_executing_command(command_name, command_args, command_type)

    command_result = execute_cmd(command_name)

    AppConfig().display_manager.print_command_result(command_name, command_result)

    agent.memory.add_command_result(command_name, command_result)

    return command_result


class PythonAppV2Runner(IRunner):
    def run(self):
        agent = load_agent()

        AppConfig().display_manager.print_hello_world(agent.name)

        # Generally in this loop, whenever an error happens, it's added to the agent's history and loop is restarted
        while True:
            with Spinner("Thinking... "):
                agent.chat(" test")

            response = validate_last_response(agent)

            # If response is none this is an error, chat again so they can react to it as the error was added to history
            if response is None:
                continue

            user_response, suggested_command = print_response(response, agent)

            # This means missing command or command name, restart loop so agent can react
            if user_response == WRONG_COMMAND:
                command_name = suggested_command['name'] if suggested_command and 'name' in suggested_command else \
                    suggested_command['command']
                agent.memory.add_error_command(command_name, WRONG_COMMAND)
                AppConfig().display_manager.print_error(WRONG_COMMAND)

                continue

            # Action denied from user or not accepted, meaning human feedback, again restart loop so agent can react
            if user_response == PERMISSION_DENIED or not user_response == PERMISSION_GRANTED:
                agent.memory.add_human_feedback(user_response)
                continue

            try:
                execute_command(suggested_command, agent)
            except Exception as e:
                agent.memory.add_error_command(suggested_command['name'],
                                               f"Error executing command {suggested_command['name']}")
            AppConfig().display_manager.print_error(suggested_command)

            AppConfig().save(agent)
