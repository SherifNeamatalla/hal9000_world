from abc import ABC, abstractmethod


class ICmd(ABC):
    @abstractmethod
    def execute(self, cmd_args, cmd_type=None):
        pass
