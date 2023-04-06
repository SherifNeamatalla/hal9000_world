from abc import ABC, abstractmethod


class IDisplay(ABC):
    @abstractmethod
    def print_agent_message(self, agent_name, message):
        pass

    @abstractmethod
    def ask_permission(self, agent_name, command):
        pass

    @abstractmethod
    def prompt_user_input(self, message=None):
        pass

    @abstractmethod
    def print_agent_goals(self, goals, personal_goals):
        pass

    @abstractmethod
    def print_executing_command(self, command_name, command_args=None, command_type=None):
        pass
