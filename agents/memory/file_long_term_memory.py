# This saves the data in a text file under STORAGE_PATH
import json
import os
from pathlib import Path

import yaml

from agents.memory.long_term_memory_interface import ILongTermMemory

STORAGE_PATH = os.path.join(Path(__file__).parent.parent.parent, "storage", "agents")


class FileLongTermMemory(ILongTermMemory):
    def __init__(self, agent_name):
        self.memory = {}
        self.agent_name = agent_name
        self.load_if_exists()

    def set(self, key, value):
        self.memory[key] = value
        self.save()

    def get(self, key):
        return self.memory[key]

    def delete(self, key):
        del self.memory[key]
        self.save()

    def get_as_string(self):
        return str(self.memory)

    def clear(self):
        self.memory = []
        self.save()

    def save(self):
        with open(os.path.join(STORAGE_PATH, self.agent_name, "long_term_memory.yaml"), "w") as f:
            yaml.dump(self.memory, f)

    def load_if_exists(self):
        file_path = os.path.join(STORAGE_PATH, self.agent_name, "long_term_memory.yaml")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.memory = yaml.safe_load(f)
