from abc import ABC, abstractmethod


class IDBManager(ABC):
    @abstractmethod
    def add(self, name, role, goals, config, long_term_memory, short_term_memory):
        pass

    @abstractmethod
    def delete(self, agent_id):
        pass

    @abstractmethod
    def update(self, agent_id, name=None, role=None, goals=None, config=None, long_term_memory=None,
               short_term_memory=None):
        pass

    @abstractmethod
    def get(self, agent_id):
        pass

    @abstractmethod
    def list(self):
        pass
