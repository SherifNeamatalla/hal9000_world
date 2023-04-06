import openai

from agents.base_agent import BaseAgent
from agents.config import AgentConfig
from prompts.prompt_loader import load_commands_set

SINGLE_USE_AGENT_TYPE = "SingleUseAgent"
DEFAULT_USER_INPUT = 'Start working on the task on hand'

SINGLE_USE_COMMANDS_SET = 'single_use_commands_set.txt'


class SingleUserAgent(BaseAgent):
    def __init__(self, name, role, prompt, save_model=False):
        config = AgentConfig(save_model=save_model, autonomous=True,
                             max_tokens=4000,
                             type=SINGLE_USE_AGENT_TYPE,
                             commands_set_path=SINGLE_USE_COMMANDS_SET,
                             default_user_input=DEFAULT_USER_INPUT)  # You can play with this value to get better results
        super().__init__(name=name, role=role,
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
