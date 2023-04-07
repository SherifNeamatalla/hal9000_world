# Define the endpoint for your service

from fastapi import HTTPException

from config.app_config import AppConfig
from server.server_agent_runner import ServerAgentRunner
from util.agents_util import load_agent_by_id


def do_list_agents():
    agents = AppConfig().db_manager.list()
    return [map_agent_from_dict(agent) for agent in agents]


def do_create_agent(name: str, role, goals, config: dict):
    agent_id = AppConfig().db_manager.add(name, role, goals, config)

    return map_agent(get_agent(agent_id))


def do_load_agent(agent_id: str):
    return map_agent(get_agent(agent_id))


def do_chat(agent_id: str, message: str):
    agent = get_agent(agent_id)

    runner = ServerAgentRunner(agent, user_response=message)

    return map_agent(runner.run())


def do_act(agent_id: str, command_response: str, command: dict):
    agent = get_agent(agent_id)

    runner = ServerAgentRunner(agent, command=command, user_response=command_response)

    return map_agent(runner.run())


def get_agent(agent_id: str):
    agent = load_agent_by_id(agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


def map_agent_from_dict(agent):
    return {
        'id': agent['id'],
        'name': agent['name'],
        'role': agent['role'],
        'config': agent['config'],
        'goals': agent['goals'],
        'chatHistory': agent['short_term_memory'],
    }
def map_agent(agent):

    return {
        'id': agent.id,
        'name': agent.name,
        'role': agent.role,
        'config': agent.config.to_dict(),
        'goals': agent.goals,
        'chatHistory': agent.short_term_memory.get_as_string(),
    }
