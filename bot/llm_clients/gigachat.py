# Примерная заготовка — нужен doc/API-ключ для финализации!
from .base import BaseLLMClient
from ..config import GIGACHAT_TOKEN

class GigaChatClient(BaseLLMClient):
    async def ask(self, prompt: str, system_prompt: str) -> str:
        # TODO: Реализовать на основе документации GigaChat API
        return "GigaChat ещё не подключён. Кинь доку — прикручу!"
