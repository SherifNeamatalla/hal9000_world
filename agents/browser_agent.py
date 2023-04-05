import openai

from agents.base_agent import BaseAgent


class BrowserAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Browser Agent", role='Web Browser agent for finding and summarizing information',
                         save_model=False, include_commands_set=False, include_constraints_resources_prompt=False,
                         include_response_format_prompt=False)

    def chat(self, messages):
        response = openai.ChatCompletion.create(
            model=self.config['model'],
            messages=messages,
            temperature=self.config['temperature'],
            max_tokens=300,
        )

        return response.choices[0].message["content"]
