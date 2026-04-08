import httpx

from .base import BaseLLMClient
from ..config import settings


class YandexLLMClient(BaseLLMClient):
    COMPLETION_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    @staticmethod
    def _build_model_uri() -> str:
        if settings.yandex_model_uri:
            return settings.yandex_model_uri
        if not settings.yandex_folder_id:
            raise RuntimeError("Не задан YANDEX_FOLDER_ID.")
        return f"gpt://{settings.yandex_folder_id}/yandexgpt-lite/latest"

    @staticmethod
    def _extract_text(data: dict) -> str:
        result = data.get("result") or {}
        alternatives = result.get("alternatives") or []
        if not alternatives:
            raise RuntimeError("YandexGPT вернул пустой ответ.")

        message = alternatives[0].get("message") or {}
        text = message.get("text") or alternatives[0].get("text")
        if not text:
            raise RuntimeError("YandexGPT вернул ответ в неожиданном формате.")
        return text.strip()

    async def ask(self, prompt: str, system_prompt: str) -> str:
        if not settings.yandex_api_key:
            raise RuntimeError("Не задан YANDEX_API_KEY.")

        headers = {
            "Authorization": f"Api-Key {settings.yandex_api_key}",
            "Content-Type": "application/json",
        }
        if settings.yandex_folder_id:
            headers["x-folder-id"] = settings.yandex_folder_id

        payload = {
            "modelUri": self._build_model_uri(),
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000,
            },
            "messages": [
                {"role": "system", "text": system_prompt},
                {"role": "user", "text": prompt},
            ],
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(self.COMPLETION_URL, headers=headers, json=payload)
            response.raise_for_status()

        return self._extract_text(response.json())
