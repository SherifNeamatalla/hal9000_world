from abc import ABC, abstractmethod


class ILongTermMemory(ABC):
    @abstractmethod
    def add(self, value):
        pass

    @abstractmethod
    def get(self, index):
        pass

    @staticmethod
    def set(self, index, value):
        pass

    @abstractmethod
    def delete(self, index):
        pass

    @abstractmethod
    def get_as_string(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load_if_exists(self):
        pass
