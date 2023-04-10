from langchain import GoogleSerperAPIWrapper, WikipediaAPIWrapper
from langchain.agents import Tool

search = GoogleSerperAPIWrapper()
wikipedia = WikipediaAPIWrapper()
websearch_tools = [
    Tool(
        name="Intermediate Answer",
        func=search.run,
        description="Useful for when you need to ask with search"
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Useful for searching information on Wikipedia"
    )
]
