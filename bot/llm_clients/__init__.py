from .base import BaseLLMClient
from .gigachat import GigaChatClient
from .yandex import YandexLLMClient
from ..config import settings

SUPPORTED_LLM_KEYS = ("gigachat", "yandex")


def _build_clients() -> dict[str, BaseLLMClient]:
    clients: dict[str, BaseLLMClient] = {}

    if settings.gigachat_auth_key:
        clients["gigachat"] = GigaChatClient()

    if settings.yandex_api_key and (settings.yandex_folder_id or settings.yandex_model_uri):
        clients["yandex"] = YandexLLMClient()

    return clients


LLM_CLIENTS = _build_clients()


def get_available_llm_keys() -> tuple[str, ...]:
    return tuple(LLM_CLIENTS.keys())
