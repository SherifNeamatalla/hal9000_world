from database.sqlite3_db_manager import SQLite3DBManager
from display.cmd_line_display import CmdLineDisplay
from server.managers.server_display_manager import ServerDisplayManager
from voice.eleven_labs_voice_manager import ElevenLabsVoiceManager

SERVER_APP_CONFIG = {
    'display_manager': ServerDisplayManager(),
    'db_manager': SQLite3DBManager(),
    'voice_manager': None,
    'save_format': None
}

PYTHON_APP_CONFIG = {
    'display_manager': CmdLineDisplay(),
    'db_manager': SQLite3DBManager(),
    'voice_manager': ElevenLabsVoiceManager(),
    'save_format': None
}

PYTHON_APP_CONFIG_NAME = 'python'
SERVER_APP_CONFIG_NAME = 'server'

APP_CONFIG_MAP = {
    SERVER_APP_CONFIG_NAME: SERVER_APP_CONFIG,
    PYTHON_APP_CONFIG_NAME: PYTHON_APP_CONFIG
}
