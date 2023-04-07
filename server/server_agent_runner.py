from config.app_config import AppConfig
from display.spinner import Spinner
from runners.runner_interface import IRunner
from util.commands_util import ask_user_command_permission


# An instance of this is created on every request
class ServerAgentRunner(IRunner):
    # constructor
    def __init__(self, agent, user_response=None, command=None):
        self.agent = agent
        self.command = command
        self.user_response = user_response

    def run(self):
        AppConfig().display_manager.print_hello_world(self.agent.name)

        if self.user_response and self.command:
            return self.run_command_response()

        return self.run_chat_process()

    def run_command_response(self):
        self.agent.act(self.command, self.user_response)

        self.agent.save()

        return self.agent

    def run_chat_process(self):
        # For the developer looking at the cmd line of the server
        with Spinner("Thinking... "):
            self.agent.chat(self.user_response)

        self.agent.think()

        return self.agent.think()
