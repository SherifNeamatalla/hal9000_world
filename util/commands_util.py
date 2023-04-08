from config.app_config import AppConfig
from config.constants import PERMISSION_DENIED, PERMISSION_GRANTED, MEMORY_COMMAND, WRONG_COMMAND, SNOWFLAKE_COMMAND, \
    USER_COMMAND


# Pretty important file, this is the skeleton that holds the agent when it comes to commands

def ask_user_command_permission(agent_name, command):
    if not command or not command['name']:
        # When agent has no output command, this usually means they're going to an infinite loop
        return WRONG_COMMAND

    return ask_for_permission(agent_name, command)


def execute_user_prompt_command(command_args, command_type):
    if command_type == 'prompt':
        user_input = AppConfig().display_manager.prompt_user_input(command_args['prompt'])
        return user_input

    return None


def ask_for_permission(name, command, autonomous=False):
    command_name = command['name']
    # These commands don't need user permission
    if command_name in [MEMORY_COMMAND, USER_COMMAND]:
        return PERMISSION_GRANTED

    if command_name == SNOWFLAKE_COMMAND:
        user_input = AppConfig().display_manager.prompt_user_input('')
        return user_input

    if not autonomous:
        command_name, user_input = AppConfig().display_manager.ask_permission(name, command)

        if user_input == 'n':
            return PERMISSION_DENIED

        if command_name == "human_feedback":
            return user_input

    return PERMISSION_GRANTED
