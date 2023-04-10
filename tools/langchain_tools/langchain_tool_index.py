from typing import List

from langchain.agents import Tool

from tools.langchain_tools.websearch_tools import websearch_tools


def langchain_tools_list() -> List[Tool]:
    result = []

    result.extend(websearch_tools)

    return result
