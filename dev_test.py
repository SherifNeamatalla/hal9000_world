import os

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

from agents.config import AgentConfig
from agents.langchain_agent import LangchainAgent
from commands.cmd import Cmd
from commands.cmd_browser import browse_website
from commands.langchain_tools.llm_tool_sets_util import get_default_langchain_toolset
from config.constants import FILES_DIR

config = AgentConfig()
agent = LangchainAgent(name="test", role="test", config=config, goals=["test"])

loader = TextLoader(os.path.join(FILES_DIR, "my_info.txt"))
test_index = VectorstoreIndexCreator().from_loaders([loader])
test = get_default_langchain_toolset()
cmd = Cmd("tst", browse_website, "description")
while True:
    user_input = input("User: ")
    print(agent.chat(user_input))
