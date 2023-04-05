# This class will be the most basic memory class. It will store the data in a dictionary.
# We can have more complex memory classes that will store the data in a database or in a file.

class BaseMemory():
    def __init__(self, agent_name):
        self.memory = []
        self.agent_name = agent_name

    def add(self, data):
        self.memory.append(data)

    def get(self):
        return self.memory

    def get_as_string(self):
        return '[' + ','.join(self.memory) + ']'

    def clear(self):
        self.memory = []
