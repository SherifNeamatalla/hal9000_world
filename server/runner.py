# Define the endpoint for your service
from fastapi import HTTPException

from database.sqlite3_repo import db_get_agent, db_add_agent


def do_create_agent(name: str, role, goals, config: dict):
    from agents.base_agent import BaseAgent

    agent = BaseAgent(name, role, config, goals);

    return db_add_agent()


def do_load_agent(id: str):
    return get_agent(name)


def do_chat(id: str, message: str):
    return get_agent(name).chat(message)


def do_act(id: str):
    return get_agent(name).act()


def do_wake(id: str):
    return get_agent(name).wake()


def get_agent(id: str):
    agent = db_get_agent(agent_name=name)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent
