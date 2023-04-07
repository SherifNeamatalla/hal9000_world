import os.path

import yaml

from agents.agents_factory import create_agent_by_type
from agents.base_agent import BASE_AGENT_TYPE
from config.constants import DEFAULT_START_PROMPT_PATH, INITIAL_USER_INPUT, PRESETS_DIR


class AgentConfig:
    # consturctor
    def __init__(self, commands_set_path=None,
                 model='gpt-3.5-turbo', max_tokens=4096,
                 temperature=0.1, top_p=1, frequency_penalty=0, presence_penalty=0,
                 include_constraints_resources_prompt=True, include_response_format_prompt=True,
                 include_commands_set=True, save_model=True, autonomous=False, type=BASE_AGENT_TYPE,
                 prompt_start_path=DEFAULT_START_PROMPT_PATH,
                 default_user_input=INITIAL_USER_INPUT, max_personal_goals=5):

        if not prompt_start_path:
            prompt_start_path = DEFAULT_START_PROMPT_PATH

        self.config_map = {
            'type': type,
            'model': model,
            'top_p': top_p,
            'save_model': save_model,
            'autonomous': autonomous,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'prompt_start_path': prompt_start_path,
            'presence_penalty': presence_penalty,
            'frequency_penalty': frequency_penalty,
            'commands_set_path': commands_set_path,
            'default_user_input': default_user_input,
            'max_personal_goals': max_personal_goals,
            'include_commands_set': include_commands_set,
            'include_response_format_prompt': include_response_format_prompt,
            'include_constraints_resources_prompt': include_constraints_resources_prompt,

        }

    def get(self, key):
        return self.config_map[key]

    def to_dict(self):
        return self.config_map

    @staticmethod
    def from_dict(dict_input):
        return AgentConfig(**dict_input)

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
