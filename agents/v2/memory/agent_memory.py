from config.constants import USER_ROLE, ASSISTANT_ROLE, SYSTEM_ROLE
from util.messages_util import create_agent_message, create_user_message, create_system_message


class AgentMemory:

    def __init__(self, chat_history=None, long_term_memory=None):
        self.chat_history = chat_history or []
        self.long_term_memory = long_term_memory or []

    def __dict__(self):
        return {
            "chat_history": self.chat_history,
            "long_term_memory": self.long_term_memory
        }

    def add_user_input(self, user_input):
        self.chat_history.append(create_user_message(user_input))

    def add_agent_input(self, agent_input):
        self.chat_history.append(create_agent_message(agent_input))

    def add_system_input(self, system_input):
        self.chat_history.append(create_system_message(system_input))

    def get_last_message(self, role):
        if not role:
            return self.chat_history[-1]

        for message in reversed(self.chat_history):
            if message['role'] == role:
                return message['content']

    def get_last_user_message(self):
        return self.get_last_message(USER_ROLE)

    def get_last_agent_message(self):
        return self.get_last_message(ASSISTANT_ROLE)

    def get_last_system_message(self):
        return self.get_last_message(SYSTEM_ROLE)

    def add_error_command(self, command_name, error):
        command_memory_entry = f"Command {command_name} failed, error:{str(error)}"

        self.chat_history.append(create_system_message(command_memory_entry))

    def add_command_result(self, command_name, command_result='None'):
        if not command_result:
            command_memory_entry = f"Unable to execute command {command_name}"
        else:
            command_memory_entry = f"Command {command_name} returned: {command_result}, save important information in " \
                                   f"memory!"

        self.chat_history.append(create_system_message(command_memory_entry))

    def add_human_feedback(self, user_input):
        result = f"Human feedback: {user_input}"
        self.chat_history.append(create_user_message(result))
