from commands.cmd_agents import CmdAgents
from commands.cmd_browser import CmdBrowser
from commands.cmd_code import CmdCode
from commands.cmd_file import CmdFile
from commands.cmd_google import CmdGoogle
from commands.cmd_snowflake import CmdSnowflake
from commands.cmd_youtube import CmdYoutube

# Here you can add new commands that you can specify in the agent command_set prompt
REGISTERED_COMMANDS_MAP = {
    'google': CmdGoogle(),
    "browser": CmdBrowser(),
    "agents": CmdAgents(),
    "file": CmdFile(),
    "code": CmdCode(),
    "youtube": CmdYoutube(),
    "snowflake": CmdSnowflake()
}
