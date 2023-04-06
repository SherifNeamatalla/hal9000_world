# This will be an entry point to all commands. The agent will use this class to execute commands.


import datetime
import json

from commands.cmd_interface import ICmd
from commands.registered_commands import REGISTERED_COMMANDS_MAP


def get_command_executor(cmd_name) -> ICmd:
    return REGISTERED_COMMANDS_MAP[cmd_name]


# # non-file is given, return instructions "Input should be a python
# # filepath, write your code to file and try again"
# elif command_name == "evaluate_code":
# return ai.evaluate_code(arguments["code"])
# elif command_name == "improve_code":
# return ai.improve_code(arguments["suggestions"], arguments["code"])
# elif command_name == "write_tests":
# return ai.write_tests(arguments["code"], arguments.get("focus"))
# elif command_name == "execute_python_file":  # Add this command
# return execute_python_file(arguments["file"])
# elif command_name == "task_complete":

def execute_cmd(command):
    cmd_name = command["name"]
    cmd_args = command.get("args", {})
    cmd_type = command.get("type", None)

    # TODO could create a cmd class for this to handle cleaning up stuff before closing if needed
    if cmd_name == "shutdown":
        return shutdown()

    executor = get_command_executor(cmd_name)
    if not executor:
        # TODO error
        return
    return executor.execute(cmd_args, cmd_type)


def shutdown():
    print("Shutting down...")
    quit()
