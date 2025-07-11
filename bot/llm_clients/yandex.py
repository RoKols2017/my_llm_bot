# Примерная заготовка — нужен doc/API-ключ для финализации!
from .base import BaseLLMClient
from ..config import YANDEX_TOKEN

class YandexLLMClient(BaseLLMClient):
    async def ask(self, prompt: str, system_prompt: str) -> str:
        # TODO: Реализовать на основе документации Yandex API
        return "Yandex LLM ещё не подключён. Кинь доку — прикручу!"
