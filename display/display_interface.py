from abc import ABC, abstractmethod


class IDisplay(ABC):
    @abstractmethod
    def print_agent_message(self, agent_name, message):
        pass

    @abstractmethod
    def print_user_message(self):
        pass

    @abstractmethod
    def ask_permission(self, agent_name, command):
        pass

    @abstractmethod
    def prompt_user_input(self, message=None):
        pass