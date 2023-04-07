import os
import shutil
from pathlib import Path

import yaml

from agents.agents_factory import create_agent_by_type
from config.constants import AGENTS_DIR

STORAGE_DIR = os.path.join(Path(__file__).parent.parent, "storage")
GENERATED_DIR = os.path.join(STORAGE_DIR, "generated")


def load_agent(agent_name):
    from agents.config import AgentConfig

    agent_path = os.path.join(AGENTS_DIR, agent_name)
    with open(os.path.join(agent_path, 'config.yaml'), 'r') as stream:
        yaml_content = yaml.safe_load(stream)
        config = AgentConfig.from_dict(yaml_content['config'])
        name = yaml_content['name']
        role = yaml_content['role']
        goals = yaml_content['goals'] if 'goals' in yaml_content else []
        personal_goals = yaml_content['personal_goals'] if 'personal_goals' in yaml_content else []

        return create_agent_by_type(name, role, config, config.get('type'), goals, personal_goals)


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
