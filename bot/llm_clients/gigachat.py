import time
import uuid

import httpx

from .base import BaseLLMClient
from ..config import settings


class GigaChatClient(BaseLLMClient):
    OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    def __init__(self) -> None:
        self._access_token: str | None = None
        self._expires_at: float = 0

    async def _get_access_token(self) -> str:
        if self._access_token and time.time() < self._expires_at - 60:
            return self._access_token

        if not settings.gigachat_auth_key:
            raise RuntimeError("Не задан GIGACHAT_AUTH_KEY.")

        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {settings.gigachat_auth_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "RqUID": str(uuid.uuid4()),
        }

        async with httpx.AsyncClient(verify=True, timeout=30) as client:
            response = await client.post(
                self.OAUTH_URL,
                headers=headers,
                data={"scope": settings.gigachat_scope},
            )
            response.raise_for_status()

        data = response.json()
        self._access_token = data["access_token"]
        self._expires_at = float(data["expires_at"])
        return self._access_token

    async def ask(self, prompt: str, system_prompt: str) -> str:
        access_token = await self._get_access_token()
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.gigachat_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }

        async with httpx.AsyncClient(verify=True, timeout=60) as client:
            response = await client.post(self.CHAT_URL, headers=headers, json=payload)
            response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
