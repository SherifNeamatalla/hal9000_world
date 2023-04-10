from typing import List, Dict

import tiktoken

from config.constants import RESPONSE_TOKEN_RESERVE
from util.messages_util import create_user_message


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


def create_chat_bot_context(model, max_tokens, user_input, full_message_history, context=None):
    # Add the short term memory of the agent, we will use token_counter ( Thank you Auto-GPT ! ) to add just the
    # right length of the short term memory, shouldn't exceed self.config.get('max_tokens')

    if context is None:
        context = []

    token_limit = max_tokens - count_message_tokens(context, model)
    send_token_limit = token_limit - RESPONSE_TOKEN_RESERVE  # 1000 tokens for the response
    next_message_to_add_index = len(full_message_history) - 1
    current_tokens_used = 0
    insertion_index = len(context)

    # Count the currently used tokens
    current_tokens_used = count_message_tokens(context, model)
    current_tokens_used += count_message_tokens([create_user_message(user_input)],
                                                model)  # Account for user input (appended later)

    while next_message_to_add_index >= 0:
        # print (f"CURRENT TOKENS USED: {current_tokens_used}")
        message_to_add = full_message_history[next_message_to_add_index]

        if not message_to_add or not message_to_add['content']:
            next_message_to_add_index -= 1
            continue

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
    context.extend([create_user_message(user_input)])

    tokens_remaining = token_limit - current_tokens_used

    return context, tokens_remaining
