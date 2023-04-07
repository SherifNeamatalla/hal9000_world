# This will be an entry point to all commands. The agent will use this class to execute commands.


from commands.cmd_interface import ICmd
from commands.registered_commands import REGISTERED_COMMANDS_MAP


def get_command_executor(cmd_name) -> ICmd:
    return REGISTERED_COMMANDS_MAP[cmd_name]


def execute_cmd(command):
    cmd_name = command["name"]
    cmd_args = command.get("args", {})
    cmd_type = command.get("type", None)

    # TODO could create a cmd class for this to handle cleaning up stuff before closing if needed
    if cmd_name == "shutdown":
        return shutdown()

    executor = get_command_executor(cmd_name)
    if not executor:
        return "Didn't find a suitable command executor for this command, check the name again."

    return executor.execute(cmd_args, cmd_type)


def shutdown():
    print("Shutting down...")
    quit()
