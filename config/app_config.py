from display.cmd_line_display import CmdLineDisplay


class AppConfig:
    _instance = None

    def __new__(cls, display_manager=CmdLineDisplay(), voice_manager=None):
        if cls._instance is None:
            cls.display_manager = display_manager
            cls.voice_manager = voice_manager
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        # Load configuration from file or environment variables
        pass

    @staticmethod
    def app_voice_manager():
        return AppConfig._instance.voice_manager

    @staticmethod
    def app_display_manager():
        return AppConfig._instance.display_manager
