from agents.config import AgentConfig
from agents.langchain_agent import LangchainAgent

config = AgentConfig()
agent = LangchainAgent(name="test", role="test", config=config, goals=["test"])

print(agent.chat("What's the weather like today?"))