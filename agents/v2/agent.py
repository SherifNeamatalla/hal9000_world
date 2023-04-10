import openai
from langchain import PromptTemplate

from agents.prompts.base_prompt_template import AppBasePromptTemplate
from agents.v2.agent_config_v2 import AgentConfigV2
from agents.v2.memory.agent_memory import AgentMemory
from prompts.prompt_loader import load_commands_set, load_prompt_template
from util.messages_util import create_system_message
from util.token_util_v2 import create_chat_bot_context


class Agent:
    def __init__(self, name: str, role: str, config: AgentConfigV2, agent_id: str = None, goals: [] = None,
                 memory: AgentMemory = None):
        if not goals:
            goals = []

        if not memory:
            memory = AgentMemory()

        self.id = agent_id
        self.name = name
        self.role = role
        self.goals = goals
        self.config = config
        self.memory = memory
        self.prompt = AppBasePromptTemplate()

    def chat(self, user_input: str):
        """Chat with the agent, this is the main method of the agent"""
        """This method will be called by the runner as a part of the chat loop"""

        # This creates relevant context based on user input, this will fetch the relevant context from the short term
        # memory , long term memory and the prompt
        context, remaining_tokens = self.create_context(user_input)

        response = openai.ChatCompletion.create(
            model=self.config.get('model'),
            messages=context,
            temperature=self.config.get('temperature'),
            max_tokens=remaining_tokens,
        )

        new_response_json = response.choices[0].message["content"]

        self.memory.add_user_input(user_input)
        self.memory.add_agent_input(new_response_json)

        return new_response_json

    def create_context(self, user_input):
        context = self.create_long_term_memory_context()

        user_input_full_prompt = PromptTemplate(
            input_variables=['user_input'],
            template=load_prompt_template("user_input_template.txt")
        ).format(user_input=user_input)

        return create_chat_bot_context(
            model=self.config.get('model'),
            max_tokens=self.config.get('max_tokens'),
            user_input=user_input_full_prompt,
            full_message_history=self.memory.chat_history,
            context=context
        )

    def create_long_term_memory_context(self):
        """Here we should retrieve commands and long term memory from pinecone"""
        return [create_system_message(self.prompt.format(
            name=self.name,
            role=self.role,
            goals=self.goals,
            commands=load_commands_set(self.config.get('toolset_name'))
        ))]

    @staticmethod
    def load_from_dict(data):
        name = data.get('name')
        role = data.get('role')
        config = AgentConfigV2.from_dict(data.get('config'))
        agent_id = data.get('id')
        goals = data.get('goals')
        memory = data.get('memory', None)

        return Agent(
            name=name,
            role=role,
            config=config,
            agent_id=agent_id,
            goals=goals,
            memory=memory
        )
