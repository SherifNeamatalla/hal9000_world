import json

from langchain.agents import tool

from util.storage_loader import get_saved_agents, load_agent, delete_agent_data


@tool("Create Agent")
def start_agent(name, task, save_for_later_use=True):
    """Starts a GPT agent with the given name and task."""
    from agents.sub_agent import SubAgent

    agent = SubAgent(name, task, None, save_for_later_use)

    return agent.wake()


@tool("List Agents")
def list_agents():
    """Lists all saved agents."""
    return json.dumps(load_agents())


@tool("Delete Agent")
def delete_agent(name):
    """Deletes the agent with the given name."""
    return delete_agent_data(name)


@tool("Message Agent")
def message_agent(name, message, input=None):
    """Messages the agent with the given name a given message."""
    if input:
        message = message + '. Input: ' + input
    agent = load_agent(name)
    return agent.chat(message)


def load_agents():
    from agents.sub_agent import SUB_AGENT_TYPE
    agents = get_saved_agents()
    result = []

    for agent in agents:
        if not agent['type'] == SUB_AGENT_TYPE:
            continue
        result.append(agent)

    return result


agents_tools = [
    start_agent,
    list_agents,
    delete_agent,
    message_agent
]
