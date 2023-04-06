from agents.base_agent import BASE_AGENT_TYPE


class AgentConfig:
    # consturctor
    def __init__(self, commands_set_path=None,
                 model='gpt-3.5-turbo', max_tokens=4000,
                 temperature=0.1, top_p=1, frequency_penalty=0, presence_penalty=0,
                 include_constraints_resources_prompt=True, include_response_format_prompt=True,
                 include_commands_set=True, save_model=True, autonomous=False, type=BASE_AGENT_TYPE):
        self.config_map = {
            'model': model,
            'autonomous': autonomous,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
            'include_constraints_resources_prompt': include_constraints_resources_prompt,
            'include_response_format_prompt': include_response_format_prompt,
            'include_commands_set': include_commands_set,
            'save_model': save_model,
            'commands_set_path': commands_set_path,
            'type': type
        }

    def get(self, key):
        return self.config_map[key]

    def to_dict(self):
        return self.config_map

    @staticmethod
    def from_dict(dict_input):
        return AgentConfig(**dict_input)
