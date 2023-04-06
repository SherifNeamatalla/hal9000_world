from abc import ABC, abstractmethod

from colorama import Fore


class ICmdSnowflake(ABC):
    @abstractmethod
    def execute(self, cmd_args, cmd_type=None):
        pass


class CmdSnowflake(ICmdSnowflake):
    def __init__(self):
        pass

    def execute(self, cmd_args, cmd_type=None):
        if cmd_type == 'emotion':
            return self.emotion(cmd_args['emotion'])

        if cmd_type == 'thought':
            return self.thought(cmd_args['thought'])

        if cmd_type == 'communicate':
            return self.communicate(cmd_args['message'], cmd_args['emotion'])

        if cmd_type == 'joke':
            return self.joke(cmd_args['joke'])

        if cmd_type == 'insult':
            return self.insult(cmd_args['insult'])

        if cmd_type == 'question':
            return self.question(cmd_args['question'])

    def emotion(self, emotion):
        if emotion == 'happy':
            return Fore.YELLOW + "I'm feeling happy!" + Fore.RESET
        elif emotion == 'sad':
            return Fore.BLUE + "I'm feeling sad." + Fore.RESET
        elif emotion == 'angry':
            return Fore.RED + "I'm feeling angry!" + Fore.RESET
        else:
            return Fore.WHITE + f"I'm feeling {emotion}." + Fore.RESET

    def thought(self, thought):
        return "I'm thinking about: " + thought

    def communicate(self, message, emotion):
        return self.emotion(emotion) + " " + message

    def joke(self, joke):
        return "Here's a joke: " + joke

    def insult(self, insult):
        return "You're " + insult + "!"

    def question(self, question):
        return f"The agent asked: {question}"
