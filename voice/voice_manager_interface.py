from abc import ABC, abstractmethod


class IVoiceManager(ABC):
    @abstractmethod
    def speak(self, text):
        pass
