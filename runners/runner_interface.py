from abc import ABC, abstractmethod


class IRunner(ABC):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_user_input(self):
        pass
