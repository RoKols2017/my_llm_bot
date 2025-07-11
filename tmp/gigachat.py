from langchain_gigachat.chat_models import GigaChat
from bot.config import settings
from .base import BaseLLMClient


class GigaChatClient(BaseLLMClient):
    def __init__(self):
        self.model = GigaChat(
            credentials=settings.gigachat_token,
            model=settings.gigachat_model,
            verify_ssl_certs=settings.verify_ssl,
            streaming=False,
        )

    def ask(self, prompt: str, system_prompt: str | None = None) -> str:
        from langchain_core.messages import HumanMessage
        messages = [HumanMessage(content=prompt)]
        return self.model.invoke(messages).content
