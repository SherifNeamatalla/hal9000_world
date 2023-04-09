from commands.langchain_tools.cmd_agents import agents_tools
from commands.langchain_tools.cmd_browser import browser_tools
from commands.langchain_tools.cmd_file import file_tools
from commands.langchain_tools.cmd_google import google_tools
from commands.langchain_tools.cmd_snowflake import snowflake_tools
from commands.langchain_tools.cmd_youtube import youtube_tools


def get_default_langchain_toolset():
    # Append lists
    tools = []
    tools.extend(agents_tools)
    tools.extend(browser_tools)
    tools.extend(file_tools)
    tools.extend(google_tools)
    tools.extend(youtube_tools)
    # tools.extend(snowflake_tools)
    return tools


def get_snowflake_langchain_toolset():
    # Append lists
    tools = []
    tools.extend(agents_tools)
    tools.extend(browser_tools)
    tools.extend(file_tools)
    tools.extend(google_tools)
    tools.extend(youtube_tools)
    tools.extend(snowflake_tools)
    return tools
