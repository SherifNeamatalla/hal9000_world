from colorama import Fore
from langchain.agents import tool


@tool("Emotion")
def emotion(agent_emotion):
    """Change the agent's emotion."""
    if agent_emotion == 'happy':
        return Fore.YELLOW + "I'm feeling happy!" + Fore.RESET
    elif agent_emotion == 'sad':
        return Fore.BLUE + "I'm feeling sad." + Fore.RESET
    elif agent_emotion == 'angry':
        return Fore.RED + "I'm feeling angry!" + Fore.RESET
    else:
        return Fore.WHITE + f"I'm feeling {agent_emotion}." + Fore.RESET


@tool("Thought")
def thought(agent_thought):
    """Think about something."""
    return "I'm thinking about: " + agent_thought


@tool("Communicate")
def communicate(message, agent_emotion):
    """Communicate with the user."""
    return emotion(agent_emotion) + " " + message


@tool("Joke")
def joke(agent_joke):
    """Tell a joke to the user."""
    return "Here's a joke: " + agent_joke


@tool("Insult")
def insult(agent_insult):
    """Insult the user."""
    return "You're " + agent_insult + "!"


@tool("Question")
def question(agent_question):
    """Ask a question to the user."""
    return f"The agent asked: {agent_question}"


snowflake_tools = [
    emotion,
    thought,
    communicate,
    joke,
    insult,
    question
]
