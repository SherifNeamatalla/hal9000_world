from config.constants import USER_ROLE, ASSISTANT_ROLE, SYSTEM_ROLE


def create_message(role, content):
    return {
        "role": role,
        "content": content
    }


def create_user_message(content: str) -> dict:
    return create_message(USER_ROLE, content)


def create_agent_message(content: str) -> dict:
    return create_message(ASSISTANT_ROLE, content)


def create_system_message(contents: str) -> dict:
    return create_message(SYSTEM_ROLE, contents)
