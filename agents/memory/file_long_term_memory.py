# This saves the data in a text file under STORAGE_PATH
import os
from pathlib import Path

from agents.memory.long_term_memory_interface import ILongTermMemory

STORAGE_PATH = os.path.join(Path(__file__).parent.parent.parent, "storage", "agents")


class FileLongTermMemory(ILongTermMemory):
    def __init__(self, agent_name):
        self.memory = []
        self.agent_name = agent_name
        self.load_if_exists()

    def add(self, value):
        self.memory.append(value)
        self.save()

    def get(self, index):
        return self.memory[index]

    def delete(self, key):
        del self.memory[key]
        self.save()

    def set(self, key, value):
        self.memory[key] = value
        self.save()

    def get_as_string(self):
        return ','.join(self.memory)

    def clear(self):
        self.memory = []
        self.save()

    def save(self):
        with open(os.path.join(STORAGE_PATH, self.agent_name, "long_term_memory.txt"), "w") as f:
            f.write(self.get_as_string())

    def load_if_exists(self):
        file_path = os.path.join(STORAGE_PATH, self.agent_name, "long_term_memory.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.memory = f.read().split(",")
