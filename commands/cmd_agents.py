from commands.cmd_interface import ICmd
from util.storage_loader import get_saved_agents, load_agent, delete_agent_data


class CmdAgents(ICmd):

    def __init__(self):
        pass

    def execute(self, cmd_args, cmd_type='search'):
        if cmd_type == 'start':
            return start_agent(cmd_args['name'], cmd_args['task'], cmd_args['prompt'],
                               cmd_args['save_for_later_use'])

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
    result_str = 'NAME|ROLE|TYPE\n'

    agents = load_agents()

    for agent in agents:
        result_str += f'{agent["name"]}|{agent["role"]}|{agent["type"]}\n'

    return load_agents()


def delete_agent(name):
    delete_agent_data(name)
    pass


def message_agent(name, message):
    agent = load_agent(name)
    agent.chat(message)
    pass


def load_agents():
    from agents.single_use_agent import SINGLE_USE_AGENT_TYPE
    agents = get_saved_agents()
    result = []

    for agent in agents:
        if not agent['type'] == SINGLE_USE_AGENT_TYPE:
            continue
        result.append(agent)

    return result
