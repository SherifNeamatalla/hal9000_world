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

    def extend(self, data):
        self.memory.extend(data)

    def get_last_message(self, role=None):
        if not role:
            return self.memory[-1]

        for i in range(len(self.memory) - 1, -1, -1):
            if self.memory[i]['role'] == role:
                return self.memory[i]['content']
        return None

    def get_as_string(self):
        return '[' + ','.join(self.memory) + ']'

    def clear(self):
        self.memory = []

    def delete_last_message(self):
        self.memory.pop()
