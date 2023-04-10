import json

from config.constants import DEFAULT_PROMPT_TEMPLATE_NAME
from prompts.prompt_loader import load_prompt_template


class AppBasePromptTemplate:
    """Just a starter simple template"""
    prompt_name = DEFAULT_PROMPT_TEMPLATE_NAME

    def format(self, **kwargs) -> str:
        prompt = load_prompt_template(self.prompt_name)

        prompt = prompt.replace("{name}", kwargs["name"])

        prompt = prompt.replace("{role}", kwargs["role"])

        prompt = prompt.replace("{goal}}", json.dumps(kwargs["goals"]))

        prompt = prompt.replace("{commands}", json.dumps(kwargs["commands"]))

        return prompt

    def _prompt_type(self):
        return "base_prompt_template"
