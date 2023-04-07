# This saves the data in a text file under STORAGE_PATH
import json
import os
from pathlib import Path

import yaml

from agents.memory.long_term_memory_interface import ILongTermMemory

STORAGE_PATH = os.path.join(Path(__file__).parent.parent.parent, "storage", "agents")


class FileLongTermMemory(ILongTermMemory):
    def __init__(self, agent_name, old_memory=""):
        self.memory = self.load_from_string(old_memory)
        self.cached_memory = []
        self.agent_name = agent_name
        # Uncomment this if u'r not using a db
        # self.load_if_exists()

    def set(self, key, value):
        self.memory[key] = value
        self.cache(key, value)
        return f"{key} in memory set to {value}"

    def get(self, key):
        self.cache(key, self.memory[key])
        return self.memory[key]

    def delete(self, key):
        del self.memory[key]

        if self.cached_memory and self.cached_memory[0]['key'] == key:
            self.cached_memory.pop(0)

        return f"Deleted {key} from memory"

    def cache(self, key, value):
        # for now allow only 1 item in cache
        if len(self.cached_memory) == 1:
            self.cached_memory.pop()
        self.cached_memory.append({
            key: value
        })

    def get_as_string(self):
        if not self.memory:
            return "Permanent memory: []"
        return 'Permanent memory: [' + str(
            ','.join(self.memory.keys()) + ']' + ', Cached Permanent Memory Key,Value: ' + (str(
                self.cached_memory)) if self.cached_memory and self.cached_memory[0] else '')

    def clear(self):
        self.memory = []

    def load_from_string(self, string):
        if not string:
            return {}
        return json.loads(string)

    def get_as_db_string(self):
        return json.dumps(self.memory)

    def load_if_exists(self):
        file_path = os.path.join(STORAGE_PATH, self.agent_name, "long_term_memory.yaml")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.memory = yaml.safe_load(f)

                if self.memory is None:
                    self.memory = {}

                self.cached_memory = []
                if self.memory and len(self.memory.keys()) > 0:
                    key = list(self.memory.keys())[-1]
                    self.cache(key, self.memory[key])
