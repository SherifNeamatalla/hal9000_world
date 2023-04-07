from abc import ABC, abstractmethod


class IDisplay(ABC):

    @abstractmethod
    def print_hello_world(self, agent_name):
        pass

    @abstractmethod
    def print_agent_message(self, agent_name, message):
        pass

    @abstractmethod
    def print_agent_goals(self, goals, personal_goals):
        pass

    @abstractmethod
    def print_agent_criticism(self, criticism):
        pass

    @abstractmethod
    def print_agent_reasoning(self, reasoning):
        pass

    @abstractmethod
    def print_agent_thoughts(self, thoughts):
        pass

    @abstractmethod
    def ask_permission(self, agent_name, command):
        pass

    @abstractmethod
    def prompt_user_input(self, message=None):
        pass

    @abstractmethod
    def print_executing_command(self, command_name, command_args=None, command_type=None):
        pass

    @abstractmethod
    def print_command_result(self, command_name, command_result):
        pass

    @abstractmethod
    def print_error(self, command_memory_entry):
        pass
