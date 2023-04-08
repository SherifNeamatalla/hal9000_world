import json

from colorama import Fore, Style

from display.display_interface import IDisplay


class ServerDisplayManager(IDisplay):

    def __init__(self):
        self.logs = []

    def reset_state(self):
        self.logs = []

    def prompt_user_input(self, message="User Input:"):
        # Not needed for this implementation
        pass

    def print_agent_message(self, agent_name, message):
        self.print(Fore.GREEN + f"{agent_name}" + Fore.WHITE + f": {message}" + Style.RESET_ALL, flush=True)

    def ask_permission(self, agent_name, command):
        command_name = command['name']
        command_args = command.get('args', {})
        command_type = command.get('type', None)
        self.print(
            Fore.WHITE + f"Requesting permission to execute command: " + Fore.GREEN + f"{command_name}" + Style.RESET_ALL,
            flush=True)

        if command_args:
            self.print(
                Fore.WHITE + f"Command arguments: " + Fore.GREEN + f"{json.dumps(command_args)}" + Style.RESET_ALL,
                flush=True)

        if command_type:
            self.print(Fore.WHITE + f"Command type: " + Fore.GREEN + f"{command_type}" + Style.RESET_ALL, flush=True)

        self.print(
            Fore.WHITE + f"Enter " + Fore.GREEN + 'y' + Fore.WHITE + f" to authorise command or " +
            Fore.RED + 'n' + Fore.WHITE + f" to exit program, or enter feedback for " + Fore.GREEN + f"{agent_name}"
            + Fore.WHITE + "...",
            flush=True)

        self.print("", is_prompt=True)

    def print_agent_goals(self, goals, personal_goals):
        self.print(Fore.YELLOW + f"Goals:" + Style.RESET_ALL, flush=True)
        for goal in goals:
            self.print(Fore.WHITE + f"{goal}" + Style.RESET_ALL, flush=True)

        self.print(Fore.YELLOW + f"Plans:" + Style.RESET_ALL, flush=True)

        for goal in personal_goals:
            self.print(Fore.WHITE + f"{goal}" + Style.RESET_ALL, flush=True)

    def print_executing_command(self, command_name, command_args, command_type):
        self.print(Fore.WHITE + f"Executing command: " + Fore.GREEN + f"{command_name}" + Style.RESET_ALL, flush=True)

        if command_args:
            self.print(
                Fore.WHITE + f"Command arguments: " + Fore.GREEN + f"{json.dumps(command_args)}" + Style.RESET_ALL,
                flush=True)

        if command_type:
            self.print(Fore.WHITE + f"Command type: " + Fore.GREEN + f"{command_type}" + Style.RESET_ALL, flush=True)

    def print_hello_world(self, agent_name):
        self.print(Fore.WHITE + f"Hello World! {agent_name} here!" + Style.RESET_ALL, flush=True)

    def print_agent_criticism(self, criticism):
        self.print(Fore.RED + f"Criticism: {criticism}" + Style.RESET_ALL, flush=True)

    def print_agent_reasoning(self, reasoning):
        self.print(Fore.CYAN + f"Reasoning: {reasoning}" + Style.RESET_ALL, flush=True)

    def print_command_result(self, command_name, command_result):
        self.print(Fore.WHITE + f"Command: " + Fore.GREEN + f"{command_name}" + Style.RESET_ALL, flush=True)

        if command_result:
            self.print(Fore.WHITE + f"Result: " + Fore.GREEN + f"{json.dumps(command_result)}" + Style.RESET_ALL,
                       flush=True)
        else:
            self.print(Fore.WHITE + f"Result: " + Fore.GREEN + f"None" + Style.RESET_ALL, flush=True)

        pass

    def print_error(self, command_memory_entry):
        self.print(Fore.RED + f"{command_memory_entry}" + Style.RESET_ALL, flush=True)

    def print_agent_thoughts(self, thoughts):
        self.print(Fore.LIGHTGREEN_EX + f"Thoughts: " + Fore.GREEN + f"{thoughts}" + Style.RESET_ALL, flush=True)

    def print(self, message, is_prompt=False, flush=False):
        self.logs.append({
            "message": message,
            "is_prompt": is_prompt
        })

        # if is_prompt:
        #     return input(message)

        print(message, flush=flush)

    def get_logs(self):
        return self.logs
