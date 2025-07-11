from .proxyapi import ProxyAPIClient
# from .yandex import YandexClient  # Пока не реализован
try:
    from .gigachat import GigaChatClient
except ImportError:
    GigaChatClient = None

LLM_CLIENTS = {
    "proxyapi": ProxyAPIClient,
    "gigachat": GigaChatClient,
    # "yandex": YandexClient
}
