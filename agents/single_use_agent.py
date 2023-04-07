import openai

from agents.base_agent import BaseAgent
from agents.config import AgentConfig
from util.token_counter import truncate_messages, count_message_tokens


class SingleUseAgent(BaseAgent):
    def __init__(self, name, role, config):
        super().__init__(name=name, role=role, config=config)

    def chat(self, user_input):
        if isinstance(user_input, list):
            context = truncate_messages(user_input, self.config.get('max_tokens'), self.config.get('model'))
            remaining_tokens = self.config.get('max_tokens') - count_message_tokens(context, self.config.get('model'))
        else:
            context, remaining_tokens = self.create_context(user_input)
        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=context,
            temperature=self.config.get('temperature'),
            max_tokens=remaining_tokens,
        )

        return response.choices[0].message["content"]
