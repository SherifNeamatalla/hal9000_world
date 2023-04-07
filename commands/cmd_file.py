import os

import requests

from commands.cmd_interface import ICmd
from util.storage_loader import GENERATED_DIR


class CmdFile(ICmd):

    def __init__(self):
        pass

    def execute(self, cmd_args, cmd_type='read'):
        if cmd_type == 'read':
            return read_file(cmd_args['file'])

        if cmd_type == 'write':
            return write_to_file(cmd_args['file'], cmd_args['text'])

        if cmd_type == 'append':
            return append_to_file(cmd_args['file'], cmd_args['text'])

        if cmd_type == 'delete':
            return delete_file(cmd_args['file'])

        if cmd_type == 'download':
            return download(cmd_args['filename'], cmd_args['url'])

        pass


def read_file(filename):
    try:
        filepath = safe_join(GENERATED_DIR, filename)
        with open(filepath, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        return "Error: " + str(e)


def download(filename, url):
    response = requests.get(url)
    filepath = safe_join(GENERATED_DIR, filename)
    with open(filepath, 'wb') as out_file:
        out_file.write(response.content)
    return "File downloaded successfully."


def write_to_file(filename, text):
    try:
        filepath = safe_join(GENERATED_DIR, filename)
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, "w") as f:
            f.write(text)
        return "File written to successfully."
    except Exception as e:
        return "Error: " + str(e)


def append_to_file(filename, text):
    try:
        filepath = safe_join(GENERATED_DIR, filename)
        with open(filepath, "a") as f:
            f.write(text)
        return "Text appended successfully."
    except Exception as e:
        return "Error: " + str(e)


def delete_file(filename):
    try:
        filepath = safe_join(GENERATED_DIR, filename)
        os.remove(filepath)
        return "File deleted successfully."
    except Exception as e:
        return "Error: " + str(e)


def safe_join(base, *paths):
    new_path = os.path.join(base, *paths)
    norm_new_path = os.path.normpath(new_path)

    if os.path.commonprefix([base, norm_new_path]) != base:
        return "Attempted to access outside of working directory."

    return norm_new_path
