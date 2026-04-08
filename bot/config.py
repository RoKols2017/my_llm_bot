import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    if value is None:
        return None
    value = value.strip()
    return value or None


@dataclass(frozen=True)
class Settings:
    bot_token: str | None
    default_llm: str
    gigachat_auth_key: str | None
    gigachat_scope: str
    gigachat_model: str
    yandex_api_key: str | None
    yandex_folder_id: str | None
    yandex_model_uri: str | None


settings = Settings(
    bot_token=_get_env("BOT_TOKEN"),
    default_llm=(_get_env("LLM_DEFAULT", "gigachat") or "gigachat").lower(),
    gigachat_auth_key=_get_env("GIGACHAT_AUTH_KEY"),
    gigachat_scope=_get_env("GIGACHAT_SCOPE", "GIGACHAT_API_PERS") or "GIGACHAT_API_PERS",
    gigachat_model=_get_env("GIGACHAT_MODEL", "GigaChat") or "GigaChat",
    yandex_api_key=_get_env("YANDEX_API_KEY"),
    yandex_folder_id=_get_env("YANDEX_FOLDER_ID"),
    yandex_model_uri=_get_env("YANDEX_MODEL_URI"),
)
