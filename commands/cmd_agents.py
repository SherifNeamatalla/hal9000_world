from commands.cmd_interface import ICmd
from util.storage_loader import get_saved_agents, load_agent, delete_agent_data


class CmdAgents(ICmd):

    def __init__(self):
        pass

    def execute(self, cmd_args, cmd_type='search'):
        if cmd_type == 'create':
            return start_agent(cmd_args['name'], cmd_args['task'], cmd_args['prompt'],
                               cmd_args['save_for_later_use'])

        if cmd_type == 'get':
            agents = list_agents()

            for agent in agents:
                if agent['name'] == cmd_args['name']:
                    return agent
            return 'Agent not found'

        if cmd_type == 'list':
            return list_agents()

        if cmd_type == 'delete':
            return delete_agent(cmd_args['name'])

        if cmd_type == 'message':
            return message_agent(cmd_args['name'], cmd_args['message'])

        pass


def start_agent(name, task, prompt, save_for_later_use=False):
    from agents.single_use_agent import SingleUserAgent

    agent = SingleUserAgent(name, task, prompt, save_for_later_use)

    return agent.wake()


def list_agents():
    return load_agents()


def delete_agent(name):
    return delete_agent_data(name)


def message_agent(name, message):
    agent = load_agent(name)
    return agent.chat(message)


def load_agents():
    from agents.single_use_agent import SINGLE_USE_AGENT_TYPE
    agents = get_saved_agents()
    result = []

    for agent in agents:
        if not agent['type'] == SINGLE_USE_AGENT_TYPE:
            continue
        result.append(agent)

    return result
