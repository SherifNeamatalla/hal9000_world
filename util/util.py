from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from config.constants import USER_ROLE, SYSTEM_ROLE, ASSISTANT_ROLE


def create_message(role, content):
    return {
        "role": role,
        "content": content
    }


def create_langchain_message(role, content):
    if role == USER_ROLE:
        return HumanMessage(content=content)

    if role == SYSTEM_ROLE:
        return SystemMessage(content=content)

    if role == ASSISTANT_ROLE:
        return AIMessage(content=content)
