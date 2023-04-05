import json

from display.display_interface import IDisplay


class CmdLineDisplay(IDisplay):
    def print_agent_message(self, agent_name, message):
        print(f"Agent {agent_name} says: {message}")

    def print_user_message(self):
        pass
