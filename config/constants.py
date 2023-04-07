import os
from pathlib import Path

####Roles####
USER_ROLE = "user"
SYSTEM_ROLE = "system"
ASSISTANT_ROLE = "assistant"

####Commands####
MEMORY_COMMAND = "memory"
USER_COMMAND = "user"
SNOWFLAKE_COMMAND = "snowflake"

####Default Prompts and Configs####
CONSTRAINTS_RESOURCES_PROMPT_NAME = "constraints_resources_prompt.txt"
RESPONSE_FORMAT_PROMPT_NAME = "response_format_prompt.txt"
BASE_COMMANDS_SET_NAME = "base_commands_set.txt"
INITIAL_USER_INPUT = 'Determine which next command to use, and respond using the format specified above:'
DEFAULT_START_PROMPT_PATH = 'default_start_prompt.txt'

####Sub agent constants####
SINGLE_USE_AGENT_TYPE = "SingleUseAgent"
SUB_AGENT_TYPE = "SubAgent"
DEFAULT_USER_INPUT = 'Start working on the task on hand'
SUB_AGENT_COMMANDS_SET = 'sub_agent_commands_set.txt'
SUB_AGENT_ROLE_PREFIX="You are an agent whose sole task is to "
####Response Errors####
ACTION_DENIED = "Action denied"
JSON_LOADING_ERROR = "parsing failed, please stick to the format specified above by the system."

####Agent Types####
BASE_AGENT_TYPE = "BaseAgent"
BROWSER_AGENT_TYPE = "BrowserAgent"

####Directories####
AGENTS_DIR = os.path.join(Path(__file__).parent.parent, "storage", "agents")
PRESETS_DIR = os.path.join(Path(__file__).parent.parent, "storage", "presets")
PROMPTS_DIR = os.path.join(Path(__file__).parent.parent, "prompts")
###Presets###
BROWSER_AGENT_PRESET_NAME = 'browser_agent_preset.yaml'
YOUTUBE_AGENT_PRESET_NAME = 'youtube_agent_preset.yaml'
