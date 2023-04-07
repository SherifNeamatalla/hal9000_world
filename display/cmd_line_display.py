import json

from colorama import Fore, Style

from display.display_interface import IDisplay


class CmdLineDisplay(IDisplay):
    def prompt_user_input(self, message="User Input:"):
        message = message if message else "User Input: "
        return input(Fore.WHITE + message + Style.RESET_ALL)

    def print_agent_message(self, agent_name, message):
        print(Fore.GREEN + f"{agent_name}" + Fore.WHITE + f": {message}" + Style.RESET_ALL, flush=True)

    def ask_permission(self, agent_name, command):
        command_name = command['name']
        command_args = command.get('args', {})
        command_type = command.get('type', None)
        print(
            Fore.WHITE + f"Requesting permission to execute command: " + Fore.GREEN + f"{command_name}" + Style.RESET_ALL,
            flush=True)

        if command_args:
            print(Fore.WHITE + f"Command arguments: " + Fore.GREEN + f"{json.dumps(command_args)}" + Style.RESET_ALL,
                  flush=True)

        if command_type:
            print(Fore.WHITE + f"Command type: " + Fore.GREEN + f"{command_type}" + Style.RESET_ALL, flush=True)

        print(
            Fore.WHITE + f"Enter " + Fore.GREEN + 'y' + Fore.WHITE + f" to authorise command or " +
            Fore.RED + 'n' + Fore.WHITE + f" to exit program, or enter feedback for " + Fore.GREEN + f"{agent_name}"
            + Fore.WHITE + "...",
            flush=True)
        console_input = input("")
        if console_input.lower() == "y":
            user_input = "y"
        elif console_input.lower() == "n":
            user_input = "n"
        else:
            user_input = console_input
            command_name = "human_feedback"

        if user_input == "y":
            print(Fore.LIGHTWHITE_EX + "-=-=-=-=-=-=-= COMMAND AUTHORISED BY USER -=-=-=-=-=-=-=" + Style.RESET_ALL)

        return command_name, user_input

    def print_agent_goals(self, goals, personal_goals):
        print(Fore.YELLOW + f"Goals:" + Style.RESET_ALL, flush=True)
        for goal in goals:
            print(Fore.WHITE + f"{goal}" + Style.RESET_ALL, flush=True)

        print(Fore.YELLOW + f"Plans:" + Style.RESET_ALL, flush=True)

        for goal in personal_goals:
            print(Fore.WHITE + f"{goal}" + Style.RESET_ALL, flush=True)

    def print_executing_command(self, command_name, command_args, command_type):
        print(Fore.WHITE + f"Executing command: " + Fore.GREEN + f"{command_name}" + Style.RESET_ALL, flush=True)

        if command_args:
            print(Fore.WHITE + f"Command arguments: " + Fore.GREEN + f"{json.dumps(command_args)}" + Style.RESET_ALL,
                  flush=True)

        if command_type:
            print(Fore.WHITE + f"Command type: " + Fore.GREEN + f"{command_type}" + Style.RESET_ALL, flush=True)

    def print_hello_world(self, agent_name):
        print(Fore.WHITE + f"Hello World! {agent_name} here!" + Style.RESET_ALL, flush=True)

    def print_agent_criticism(self, criticism):
        print(Fore.RED + f"Criticism: {criticism}" + Style.RESET_ALL, flush=True)

    def print_agent_reasoning(self, reasoning):
        print(Fore.CYAN + f"Reasoning: {reasoning}" + Style.RESET_ALL, flush=True)

    def print_command_result(self, command_name, command_result):
        print(Fore.WHITE + f"Command: " + Fore.GREEN + f"{command_name}" + Style.RESET_ALL, flush=True)

        if command_result:
            print(Fore.WHITE + f"Result: " + Fore.GREEN + f"{json.dumps(command_result)}" + Style.RESET_ALL, flush=True)
        else:
            print(Fore.WHITE + f"Result: " + Fore.GREEN + f"None" + Style.RESET_ALL, flush=True)

        pass

    def print_error(self, command_memory_entry):
        print(Fore.RED + f"{command_memory_entry}" + Style.RESET_ALL, flush=True)

    def print_agent_thoughts(self, thoughts):
        print(Fore.LIGHTGREEN_EX + f"Thoughts: " + Fore.GREEN + f"{thoughts}" + Style.RESET_ALL, flush=True)
