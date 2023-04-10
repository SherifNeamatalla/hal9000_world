import os

import requests

from tools.tool_annotation import app_tool
from util.storage_loader import GENERATED_DIR


@app_tool("Write to File")
def read_file(filename):
    """Reads a file from the generated directory."""
    try:
        filepath = safe_join(GENERATED_DIR, filename)
        with open(filepath, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        return "Error: " + str(e)


@app_tool("Download File")
def download(filename, url):
    """Downloads a file from a URL and saves it in the generated directory."""
    response = requests.get(url)
    filepath = safe_join(GENERATED_DIR, filename)
    with open(filepath, 'wb') as out_file:
        out_file.write(response.content)
    return "File downloaded successfully."


@app_tool("Write to File")
def write_to_file(filename, text):
    """Writes text to a file in the generated directory."""
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


@app_tool("Append to File")
def append_to_file(filename, text):
    """Appends text to a file in the generated directory."""
    try:
        filepath = safe_join(GENERATED_DIR, filename)
        with open(filepath, "a") as f:
            f.write(text)
        return "Text appended successfully."
    except Exception as e:
        return "Error: " + str(e)


@app_tool("Delete File")
def delete_file(filename):
    """Deletes a file from the generated directory."""
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


file_tools = [
    read_file,
    download,
    write_to_file,
    append_to_file,
    delete_file,
]
