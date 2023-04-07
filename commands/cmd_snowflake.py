from colorama import Fore

from commands.cmd_interface import ICmd


class CmdSnowflake(ICmd):
    def __init__(self):
        pass

    def execute(self, cmd_args, cmd_type=None):
        if cmd_type == 'emotion':
            return emotion(cmd_args['emotion'])

        if cmd_type == 'thought':
            return thought(cmd_args['thought'])

        if cmd_type == 'communicate':
            return communicate(cmd_args['message'], cmd_args['emotion'])

        if cmd_type == 'joke':
            return joke(cmd_args['joke'])

        if cmd_type == 'insult':
            return insult(cmd_args['insult'])

        if cmd_type == 'question':
            return question(cmd_args['question'])


def emotion(agent_emotion):
    if agent_emotion == 'happy':
        return Fore.YELLOW + "I'm feeling happy!" + Fore.RESET
    elif agent_emotion == 'sad':
        return Fore.BLUE + "I'm feeling sad." + Fore.RESET
    elif agent_emotion == 'angry':
        return Fore.RED + "I'm feeling angry!" + Fore.RESET
    else:
        return Fore.WHITE + f"I'm feeling {agent_emotion}." + Fore.RESET


def thought(agent_thought):
    return "I'm thinking about: " + agent_thought


def communicate(message, agent_emotion):
    return emotion(agent_emotion) + " " + message


def joke(agent_joke):
    return "Here's a joke: " + agent_joke


def insult(agent_insult):
    return "You're " + agent_insult + "!"


def question(agent_question):
    return f"The agent asked: {agent_question}"
