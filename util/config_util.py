# This can be called by the entry point of the app
# either main.py for running it as python app, or server/server.py for running it as a server
# or whatever other modes you add, make sure to change CURRENT_MODE env variable to the correct mode
import os

from config.saved_app_configs import APP_CONFIG_MAP


def init_app_config():
    from config.app_config import AppConfig
    from database.sqlite3_db_manager import SQLite3DBManager
    from display.cmd_line_display import CmdLineDisplay

    config = APP_CONFIG_MAP[os.environ['CURRENT_MODE']]

    AppConfig(**config)
