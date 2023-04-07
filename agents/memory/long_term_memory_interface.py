from abc import ABC, abstractmethod


class ILongTermMemory(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @staticmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def get_as_string(self):
        pass

    @abstractmethod
    def clear(self):
        pass
