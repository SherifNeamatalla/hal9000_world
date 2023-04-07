import json
import os
from typing import List

import docker as docker

from commands.cmd_interface import ICmd

#TODO:implement this
class CmdCode(ICmd):

    def __init__(self):
        pass

    def execute(self, cmd_args, cmd_type='read'):

        if cmd_type == 'evaluate':
            return evaluate_code(cmd_args['file'])

        if cmd_type == 'improve':
            return improve_code(cmd_args['suggestions'], cmd_args['code'])

        if cmd_type == 'tests':
            return write_tests(cmd_args['code'], cmd_args['focus'])

        if cmd_type == 'execute':
            return execute_file(cmd_args['file'], cmd_args['args'])


# Evaluating code

def evaluate_code(code: str) -> List[str]:
    function_string = "def analyze_code(code: str) -> List[str]:"
    args = [code]
    description_string = """Analyzes the given code and returns a list of suggestions for improvements."""

    result_string = call_ai_function(function_string, args, description_string)

    return result_string


# Improving code

def improve_code(suggestions: List[str], code: str) -> str:
    function_string = (
        "def generate_improved_code(suggestions: List[str], code: str) -> str:"
    )
    args = [json.dumps(suggestions), code]
    description_string = """Improves the provided code based on the suggestions provided, making no other changes."""

    result_string = call_ai_function(function_string, args, description_string)
    return result_string


# Writing tests


def write_tests(code: str, focus: List[str]) -> str:
    function_string = (
        "def create_test_cases(code: str, focus: Optional[str] = None) -> str:"
    )
    args = [code, json.dumps(focus)]
    description_string = """Generates test cases for the existing code, focusing on specific areas if required."""

    result_string = call_ai_function(function_string, args, description_string)
    return result_string


def execute_file(file: str, args):
    if not args['language'] == 'py':
        return "Error: Invalid language. Only Python is supported."

    return execute_python_file(file)


def execute_python_file(file):
    workspace_folder = "auto_gpt_workspace"

    print(f"Executing file '{file}' in workspace '{workspace_folder}'")

    if not file.endswith(".py"):
        return "Error: Invalid file type. Only .py files are allowed."

    file_path = os.path.join(workspace_folder, file)

    if not os.path.isfile(file_path):
        return f"Error: File '{file}' does not exist."

    try:
        client = docker.from_env()

        # You can replace 'python:3.8' with the desired Python image/version
        # You can find available Python images on Docker Hub:
        # https://hub.docker.com/_/python
        container = client.containers.run(
            'python:3.10',
            f'python {file}',
            volumes={
                os.path.abspath(workspace_folder): {
                    'bind': '/workspace',
                    'mode': 'ro'}},
            working_dir='/workspace',
            stderr=True,
            stdout=True,
            detach=True,
        )

        output = container.wait()
        logs = container.logs().decode('utf-8')
        container.remove()

        # print(f"Execution complete. Output: {output}")
        # print(f"Logs: {logs}")

        return logs

    except Exception as e:
        return f"Error: {str(e)}"


def call_ai_function(function_string: str, args: List[str], description_string: str) -> str:
    # TODO
    pass
