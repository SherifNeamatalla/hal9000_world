# This class will be the most basic memory class. It will store the data in a dictionary.
# We can have more complex memory classes that will store the data in a database or in a file.
import json

from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict


class LangchainMemory:
    def __init__(self, agent_name, old_memory=None):
        self.memory = ConversationBufferMemory(
            return_messages=True,
        )

        if old_memory:
            messages = messages_from_dict(old_memory)
            self.memory.chat_memory.messages = messages

        self.agent_name = agent_name

    def add_user_message(self, message):
        self.memory.chat_memory.add_user_message(message)

    def add_agent_message(self, message):
        self.memory.chat_memory.add_ai_message(message)

    def get(self, inputs=None):
        if inputs is None:
            inputs = {}
        return self.memory.load_memory_variables(inputs)

    def extend(self, data):
        self.memory.extend(data)

    def get_last_message(self, role=None):
        if not self.memory:
            return None
        if not role:
            return self.memory[-1]

        for i in range(len(self.memory) - 1, -1, -1):
            if self.memory[i]['role'] == role:
                return self.memory[i]['content']
        return None

    def get_as_string(self):
        return self.memory

    # list to string

    def load_from_string(self, string):
        if not string:
            return []
        return json.loads(string)

    # reverse get_as_string

    def clear(self):
        self.memory = []

    def delete_last_message(self):
        self.memory.pop()

    def get_messages(self):
        return self.memory.chat_memory.messages
