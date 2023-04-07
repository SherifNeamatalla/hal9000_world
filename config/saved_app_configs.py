from config.app_config import AppConfig
from database.sqlite3_db_manager import SQLite3DBManager
from display.cmd_line_display import CmdLineDisplay

SERVER_APP_CONFIG = {
    'display_manager': CmdLineDisplay(),
    'db_manager': SQLite3DBManager(),
    'voice_manager': None,
    'save_format': None
}

PYTHON_APP_CONFIG = {
    'display_manager': CmdLineDisplay(),
    'db_manager': SQLite3DBManager(),
    'voice_manager': None,
    'save_format': None
}

APP_CONFIG_MAP = {
    'server': SERVER_APP_CONFIG,
    'python': PYTHON_APP_CONFIG
}
