import os
from pathlib import Path
import shutil
import yaml

STORAGE_DIR = os.path.join(Path(__file__).parent.parent, "storage")
AGENTS_DIR = os.path.join(STORAGE_DIR, "agents")
GENERATED_DIR = os.path.join(STORAGE_DIR, "generated")


def load_agent(agent_name):
    from agents.base_agent import BASE_AGENT_TYPE, BaseAgent
    from agents.browser_agent import BROWSER_AGENT_TYPE, BrowserAgent
    from agents.single_use_agent import SINGLE_USE_AGENT_TYPE, SingleUserAgent
    from agents.config import AgentConfig

    agent_path = os.path.join(AGENTS_DIR, agent_name)
    with open(os.path.join(agent_path, 'config.yaml'), 'r') as stream:
        yaml_content = yaml.safe_load(stream)
        config = AgentConfig.from_dict(yaml_content['config'])
        name = yaml_content['name']
        role = yaml_content['role']

        if config.get('type') == BROWSER_AGENT_TYPE:
            return BrowserAgent()

        if config.get('type') == SINGLE_USE_AGENT_TYPE:
            return SingleUserAgent(name, role, config.get('save_model'))

        if config.get('type') == BASE_AGENT_TYPE:
            return BaseAgent(name, role, config)

        return BaseAgent(name, role, config)


def get_saved_agents():
    from agents.config import AgentConfig
    # loop on all folders under agents, try to parse their config, if it fails ignore them, if not fail parse
    # config.yaml and return a list of agents
    agents = []
    for agent in os.listdir(AGENTS_DIR):
        try:
            agent_path = os.path.join(AGENTS_DIR, agent)
            with open(os.path.join(agent_path, 'config.yaml'), 'r') as stream:
                yaml_content = yaml.safe_load(stream)
                config = AgentConfig.from_dict(yaml_content['config'])
                name = yaml_content['name']
                role = yaml_content['role']
                agents.append({"name": name, "role": role, "type": config.get('type')})
        except:
            pass

    return agents


def delete_agent_data(agent_name):
    agent_path = os.path.join(AGENTS_DIR, agent_name)
    try:
        os.remove(agent_path)
        return 'Agent deleted successfully'
    except:
        shutil.rmtree(agent_path)
        return 'Agent deleted successfully'
