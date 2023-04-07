# Define the endpoint for your service

from fastapi import HTTPException

from config.app_config import AppConfig
from util.agents_util import load_agent_by_id


def do_create_agent(name: str, role, goals, config: dict):
    agent_id = AppConfig().db_manager.add(name, role, goals, config)

    return map_agent(get_agent(agent_id))


def do_load_agent(agent_id: str):
    return map_agent(get_agent(agent_id))


def do_chat(agent_id: str, message: str):
    agent = get_agent(agent_id)
    agent.chat(message)
    return map_agent(agent)


def do_act(agent_id: str, command: dict):
    agent = get_agent(agent_id)
    agent.think(command)
    return map_agent(agent)


def do_loop(agent_id: str, message: str):
    agent = get_agent(agent_id)
    agent.chat(message)
    agent.think()
    agent.act()
    return map_agent(agent)


def do_wake(agent_id: str):
    agent = get_agent(agent_id)
    agent.wake()
    return map_agent(agent)


def get_agent(agent_id: str):
    agent = load_agent_by_id(agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


def map_agent(agent):
    return {
        'id': agent.id,
        'name': agent.name,
        'role': agent.role,
        'config': agent.config.to_dict(),
        'goals': agent.goals,
        'short_term_memory': agent.short_term_memory,
    }
