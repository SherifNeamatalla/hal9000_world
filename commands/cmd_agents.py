from commands.cmd_interface import ICmd
from storage.storage_loader import get_saved_agents, load_agent


class CmdAgents(ICmd):

    def __init__(self):
        self.agents = {}
        self.load_agents()
        pass

    def execute(self, cmd_args, cmd_type='search'):
        if cmd_type == 'start':
            return self.start_agent(cmd_args['name'], cmd_args['task'], cmd_args['prompt'],
                                    cmd_args['save_for_later_use'])

        if cmd_type == 'list':
            return self.list_agents()

        if cmd_type == 'delete':
            return self.delete_agent(cmd_args['name'])

        if cmd_type == 'message':
            return self.message_agent(cmd_args['name'], cmd_args['message'])

        pass

    def start_agent(self, name, task, prompt, save_for_later_use=False):
        pass

    def list_agents(self):
        pass

    def delete_agent(self, name):
        pass

    def message_agent(self, name, message):
        agent = load_agent(name)
        agent.chat(message)
        pass

    def load_agents(self):
        agents = get_saved_agents()
        result_str = 'NAME|ROLE|TYPE'
        for agent in agents:
            result_str += f'{agent.name}|{agent.role}|{agent.type}\n'

        return result_str
