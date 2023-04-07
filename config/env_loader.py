import openai


def load_env():
    from dotenv import load_dotenv
    load_dotenv()
    import os
    openai.api_key = os.getenv("OPENAI_API_KEY")
