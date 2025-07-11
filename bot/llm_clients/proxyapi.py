import httpx
from .base import BaseLLMClient
from ..config import PROXYAPI_TOKEN

class ProxyAPIClient(BaseLLMClient):
    BASE_URL = "https://api.proxyapi.ru/openai/v1/chat/completions"

    async def ask(self, prompt: str, system_prompt: str) -> str:
        headers = {"Authorization": f"Bearer {PROXYAPI_TOKEN}"}
        payload = {
            "model": "gpt-4o",  # Или gpt-3.5-turbo, если тариф не позволяет gpt-4o
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.BASE_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
