import os.path

import yaml

from agents.agents_factory import create_agent_by_type
from config.constants import PRESETS_DIR, DEFAULT_MODEL, \
    BASE_AGENT_V2_TYPE, DEFAULT_TOOLSET_NAME


class AgentConfigV2:
    def __init__(self, agent_type=BASE_AGENT_V2_TYPE, model=DEFAULT_MODEL, max_tokens=4096, temperature=0,
                 autonomous=False, toolset_name=DEFAULT_TOOLSET_NAME):

        self.config_map = {
            'type': agent_type,
            'model': model,
            'autonomous': autonomous,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'toolset_name': toolset_name,
        }

    def get(self, key):
        return self.config_map[key]

    def to_dict(self):
        return self.config_map

    def __dict__(self):
        return self.config_map

    @staticmethod
    def from_dict(dict_input):
        return AgentConfigV2(**dict_input)

    @staticmethod
    def from_preset(name):
        path = os.path.join(PRESETS_DIR, name)

        if not os.path.exists(path):
            raise Exception("Preset file does not exist")

        with open(path, 'r') as stream:
            try:
                preset = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise Exception("Error loading preset file: " + str(exc))

            config = preset['config']

            name = preset['name']
            role = preset['role']
            agent_type = config['type']

            return create_agent_by_type(name, role, config, agent_type)
