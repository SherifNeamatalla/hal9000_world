AGENTS_DIR = os.path.join(Path(__file__).parent, "agents")


def load_agent(agent_name):
    agent_path = os.path.join(AGENTS_DIR, agent_name)
    with open(os.path.join(agent_path, 'config.yaml'), 'r') as stream:
        yaml_content = yaml.safe_load(stream)
        config = AgentConfig.from_dict(yaml_content['config'])
        name = yaml_content['name']
        role = yaml_content['role']

        if config.get('type') == BROWSER_AGENT_TYPE:
            return BrowserAgent(name, role, config)

        if config.get('type') == SINGLE_USE_AGENT_TYPE:
            return SingleUserAgent(name, role, config)

        if config.get('type') == BASE_AGENT_TYPE:
            return BaseAgent(name, role, config)

        return BaseAgent(name, role, config)


def get_saved_agents():
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
                agents.append({name: name, role: role, type: config.get('type')})
        except:
            pass

    return agents
