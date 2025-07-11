from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    @abstractmethod
    async def ask(self, prompt: str, system_prompt: str) -> str:
        pass
