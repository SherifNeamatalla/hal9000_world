import openai

from agents.base_agent import BaseAgent
from agents.config import AgentConfig
from config.constants import SUB_AGENT_TYPE, SUB_AGENT_COMMANDS_SET, DEFAULT_USER_INPUT, SUB_AGENT_ROLE_PREFIX


class SubAgent(BaseAgent):
    def __init__(self, name, role, prompt, save_model=False):
        config = AgentConfig(save_model=save_model, autonomous=True,
                             max_tokens=4096,
                             type=SUB_AGENT_TYPE,
                             include_constraints_resources_prompt=False,
                             include_response_format_prompt=False,
                             commands_set_path=SUB_AGENT_COMMANDS_SET,
                             default_user_input=DEFAULT_USER_INPUT)  # You can play with this value to get better results
        super().__init__(name=name, role=SUB_AGENT_ROLE_PREFIX + role,
                         config=config)
        # TODO test how gpt generates its prompt and change this accordingly
        # self.hello_world = self.hello_world + '\n' + prompt
        self.hello_world = self.hello_world

    def chat(self, user_input):
        context, remaining_tokens = self.create_context(user_input)

        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=context,
            temperature=self.config.get('temperature'),
            max_tokens=remaining_tokens,
        )

        return response.choices[0].message["content"]
