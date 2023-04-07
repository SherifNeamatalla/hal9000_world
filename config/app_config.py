import os

import yaml

from config.constants import AGENTS_DIR
from database.sqlite3_db_manager import SQLite3DBManager
from display.cmd_line_display import CmdLineDisplay


class AppConfig:
    _instance = None

    def __new__(cls, display_manager=CmdLineDisplay(), voice_manager=None, db_manager=SQLite3DBManager(),
                save_format=None):
        if cls._instance is None:
            cls.display_manager = display_manager
            cls.voice_manager = voice_manager
            cls.db_manager = db_manager
            cls.save_format = save_format
            cls._instance = super().__new__(cls)
        return cls._instance

    def app_voice_manager(self):
        return self.voice_manager

    def app_display_manager(self):
        return self.display_manager

    def load(self):
        pass

    def save(self, agent):
        agent_id = agent.id
        name = agent.name
        role = agent.role
        config = agent.config
        goals = agent.goals
        personal_goals = agent.personal_goals
        long_term_memory = agent.long_term_memory.get_as_db_string()
        short_term_memory = agent.short_term_memory.get_as_string()
        self.save_files(agent_id, name, role, config, goals, personal_goals)

        if AppConfig._instance.db_manager is not None:
            AppConfig._instance.db_manager.update(agent_id, name, role, goals, config, long_term_memory,
                                                  short_term_memory)

    def save_files(self, agent_id, name, role, config, goals, personal_goals):
        if self.save_format == 'yaml':
            agent_path = os.path.join(AGENTS_DIR, name)
            # create new dir if not exists
            if not os.path.exists(AGENTS_DIR):
                os.makedirs(AGENTS_DIR)

            if not os.path.exists(agent_path):
                os.makedirs(agent_path)

            with open(os.path.join(agent_path, 'config.yaml'), 'w') as outfile:
                yaml_content = {
                    "id": agent_id,
                    "name": name,
                    "role": role,
                    "model": config.get('model'),
                    "config": config.to_dict(),
                    "goals": goals,
                    "personal_goals": personal_goals
                }
                yaml.dump(yaml_content, outfile, default_flow_style=False)
