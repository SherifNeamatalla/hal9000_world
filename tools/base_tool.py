from typing import Callable, Optional, Awaitable, Any


# Copied from langchain commands
class BaseTool:
    """Command that takes in function or coroutine directly."""

    description: str = ""
    func: Callable
    coroutine: Optional[Callable[[str], Awaitable[str]]] = None

    def __init__(self, name: str, func: Callable, description: str, **kwargs: Any) -> None:
        self.name = name
        self.func = func
        self.description = description
        self.kwargs = kwargs

    def run(self, command_input: str) -> str:
        """Use the command."""
        return self.func(command_input)

    async def arun(self, command_input: str) -> str:
        """Use the command asynchronously."""
        if self.coroutine:
            return await self.coroutine(command_input)
        raise NotImplementedError("Command does not support async")
