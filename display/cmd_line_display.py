import json

from display.display_interface import IDisplay


class CmdLineDisplay(IDisplay):
    def prompt_user_input(self, message="User Input: "):
        return input(message)

    def print_agent_message(self, agent_name, message):
        print(f"Agent {agent_name} says: {message}")

    def print_user_message(self):
        pass

    def ask_permission(self, agent_name, command):
        command_name = command['name']
        command_args = command.get('args', {})
        print(f"COMMAND = {command_name} ARGUMENTS = {command_args}")
        print(
            f"Enter 'y' to authorise command or 'n' to exit program, or enter feedback for {agent_name}...",
            flush=True)
        while True:
            console_input = input("Input:")
            if console_input.lower() == "y":
                user_input = "y"
                break
            elif console_input.lower() == "n":
                user_input = "n"
                break
            else:
                user_input = console_input
                command_name = "human_feedback"
                break

        if user_input == "y NEXT COMMAND JSON":
            print("-=-=-=-=-=-=-= COMMAND AUTHORISED BY USER -=-=-=-=-=-=-=")
        elif user_input == "n":
            print("Exiting...", flush=True)
        pass
        return command_name, user_input
