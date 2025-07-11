from .proxyapi import ProxyAPIClient
from .gigachat import GigaChatClient
from .yandex import YandexLLMClient

LLM_CLIENTS = {
    "proxyapi": ProxyAPIClient(),
    "gigachat": GigaChatClient(),
    "yandex": YandexLLMClient()
}
