import openai

from agents.base_agent import BaseAgent
from agents.config import AgentConfig


BROWSER_AGENT_TYPE = "BrowserAgent"

class BrowserAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(save_model=False, include_commands_set=False, include_constraints_resources_prompt=False,
                             include_response_format_prompt=False, autonomous=True)
        super().__init__(name="Browser Agent", role='Web Browser agent for finding and summarizing information',
                         config=config)

    def chat(self, user_input):
        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=user_input,
            temperature=self.config.get('temperature'),
            max_tokens=300,
        )

        return response.choices[0].message["content"]
