from abc import ABC, abstractmethod


class IDisplay(ABC):
    @abstractmethod
    def print_agent_message(self, agent_name, message):
        pass

    @abstractmethod
    def print_user_message(self):
        pass
