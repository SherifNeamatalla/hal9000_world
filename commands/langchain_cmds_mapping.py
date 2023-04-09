from langchain.agents import Tool
from commands.registered_commands import REGISTERED_COMMANDS_MAP

langchain_tools = [
    Tool(
        name="Search",
        func=REGISTERED_COMMANDS_MAP["google"].search,
        description="Make a Google search and get top results"
    ),
    Tool(
        name="Browser",
        func=REGISTERED_COMMANDS_MAP["browser"].search,
        description="Open a browser, ask a question and get a summary of the page"
    )
]