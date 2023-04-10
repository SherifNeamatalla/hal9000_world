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
INITIAL_USER_INPUT = 'Think and determine which next command to use, and respond using ONLY the format specified ' \
                     'above, no verbose, no extra information, no extra commands, no extra thoughts, no confirmation ' \
                     'that you understood, only reply in JSON format.'
DEFAULT_START_PROMPT_PATH = 'default_start_prompt.txt'
DEFAULT_TOOLSET_NAME = "base_commands_set.txt"
DEFAULT_PROMPT_TEMPLATE_NAME = "base_prompt_template.txt"
####Sub agent constants####
SINGLE_USE_AGENT_TYPE = "SingleUseAgent"
SUB_AGENT_TYPE = "SubAgent"
DEFAULT_USER_INPUT = 'Start working on the task on hand'
SUB_AGENT_COMMANDS_SET = 'sub_agent_commands_set.txt'
SUB_AGENT_ROLE_PREFIX = "You are an agent whose sole task is to "
####Response Errors####
PERMISSION_DENIED = "Action denied"
PERMISSION_GRANTED = "Permission granted"
WRONG_COMMAND = "The command is not quite right, check the format in the commands specified above, the format has to " \
                "match it exactly don't be verbose."
JSON_LOADING_ERROR = "parsing failed, please stick to the format specified above by the system,no verbose, no extra information, no extra commands, no extra thoughts, no confirmation ' \
                     'that you understood, only reply in JSON format."

####Agent Types####
BASE_AGENT_TYPE = "BaseAgent"
BROWSER_AGENT_TYPE = "BrowserAgent"

####Directories####
AGENTS_DIR = os.path.join(Path(__file__).parent.parent, "storage", "agents")
PRESETS_DIR = os.path.join(Path(__file__).parent.parent, "storage", "presets")
FILES_DIR = os.path.join(Path(__file__).parent.parent, "storage", "files")
PROMPTS_DIR = os.path.join(Path(__file__).parent.parent, "prompts")
PROMPTS_TEMPLATES_DIR = os.path.join(Path(__file__).parent.parent, "prompts", "templates")
###Presets###
BROWSER_AGENT_PRESET_NAME = 'browser_agent_preset.yaml'
YOUTUBE_AGENT_PRESET_NAME = 'youtube_agent_preset.yaml'

###SQlite3###
HELLO_WORLD_DB_PATH = os.path.join(Path(__file__).parent.parent, "storage", "database", "hello_world.sqlite")

###Models###
DEFAULT_MODEL = "gpt-3.5-turbo"

##Agents V2 Types###
BASE_AGENT_V2_TYPE = "BaseAgentV2"
LANGCHAIN_AGENT_V2_TYPE = "LangChainAgentV2"

###Constants for the new agents###
RESPONSE_TOKEN_RESERVE = 1000
