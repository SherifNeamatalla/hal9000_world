# Agents factory

from config.constants import BROWSER_AGENT_TYPE, SUB_AGENT_TYPE, BASE_AGENT_TYPE, SINGLE_USE_AGENT_TYPE


def create_agent_by_type(name, role, config, type, goals=[], personal_goals=[]):
    from agents.base_agent import BaseAgent
    from agents.single_use_agent import SingleUseAgent
    from agents.sub_agent import SubAgent
    if type == SINGLE_USE_AGENT_TYPE:
        return SingleUseAgent(name, role, config)

    if type == SUB_AGENT_TYPE:
        return SubAgent(name, role, config.get('save_model'))

    if type == BASE_AGENT_TYPE:
        return BaseAgent(name, role, config, goals, personal_goals)
