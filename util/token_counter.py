from typing import List, Dict

import tiktoken
from config.constants import USER_ROLE
from util.util import create_message


def create_short_term_memory_context(model, max_tokens, context, user_input, full_message_history):
    # Add the short term memory of the agent, we will use token_counter ( Thank you Auto-GPT ! ) to add just the
    # right length of the short term memory, shouldn't exceed self.config.get('max_tokens')

    token_limit = max_tokens - count_message_tokens(context, model)
    send_token_limit = token_limit - 1000
    next_message_to_add_index = len(full_message_history) - 1
    current_tokens_used = 0
    insertion_index = len(context)

    # Count the currently used tokens
    current_tokens_used = count_message_tokens(context, model)
    current_tokens_used += count_message_tokens([create_message(USER_ROLE, user_input)],
                                                model)  # Account for user input (appended later)

    while next_message_to_add_index >= 0:
        # print (f"CURRENT TOKENS USED: {current_tokens_used}")
        message_to_add = full_message_history[next_message_to_add_index]

        tokens_to_add = count_message_tokens([message_to_add], model)
        if current_tokens_used + tokens_to_add > send_token_limit:
            break

        # Add the most recent message to the start of the current context, after the two system prompts.
        context.insert(insertion_index, full_message_history[next_message_to_add_index])

        # Count the currently used tokens
        current_tokens_used += tokens_to_add

        # Move to the next most recent message in the full message history
        next_message_to_add_index -= 1

    # Append user input, the length of this is accounted for above
    context.extend([create_message(USER_ROLE, user_input)])

    tokens_remaining = token_limit - current_tokens_used

    return context, tokens_remaining


def truncate_text(text: str, max_tokens: int, model_name: str) -> str:
    """
    Truncate the input text to a specified maximum number of tokens.

    Args:
    text (str): The input text to be truncated.
    max_tokens (int): The maximum number of tokens allowed in the truncated text.
    model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
    str: The truncated text.
    """
    token_count = count_string_tokens(text, model_name)

    if token_count <= max_tokens:
        return text

    truncated_text = ""
    current_tokens = 0

    words = text.split()
    for word in words:
        word_token_count = count_string_tokens(word, model_name)
        if current_tokens + word_token_count <= max_tokens:
            truncated_text += word + " "
            current_tokens += word_token_count
        else:
            break

    return truncated_text.strip()


def truncate_messages(messages: List[Dict[str, str]], max_tokens: int, model_name: str) -> List[Dict[str, str]]:
    """
    Truncate the 'content' in each message dictionary to a specified maximum number of tokens.

    Args:
    messages (List[Dict[str, str]]): A list of message dictionaries, each containing 'role' and 'content' keys.
    max_tokens (int): The maximum number of tokens allowed in the truncated 'content'.
    model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
    List[Dict[str, str]]: A list of message dictionaries with truncated 'content'.
    """

    truncated_messages = []
    max_tokens = max_tokens - 1000  # Account for the two system prompts
    for message in messages:
        truncated_content = truncate_text(message['content'], max_tokens, model_name)
        truncated_message = {'role': message['role'], 'content': truncated_content}
        truncated_messages.append(truncated_message)

    return truncated_messages

def count_message_tokens(messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo-0301") -> int:
    """
    Returns the number of tokens used by a list of messages.

    Args:
    messages (list): A list of messages, each of which is a dictionary containing the role and content of the message.
    model (str): The name of the model to use for tokenization. Defaults to "gpt-3.5-turbo-0301".

    Returns:
    int: The number of tokens used by the list of messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        # !Node: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return count_message_tokens(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        # !Note: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return count_message_tokens(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def count_string_tokens(string: str, model_name: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
    string (str): The text string.
    model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
    int: The number of tokens in the text string.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
