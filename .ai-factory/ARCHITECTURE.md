# Architecture: Layered Architecture

## Overview
This project uses a lightweight layered architecture because it is a small single-process Telegram bot with limited domain complexity and no persistence layer. The current structure already maps cleanly to practical layers without introducing extra abstractions.

The goal is to keep day-to-day development simple: Telegram handlers receive input, configuration provides runtime settings, provider clients isolate external API calls, and the startup module wires everything together. If the bot grows, these layers can be refined further without a disruptive rewrite.

## Decision Rationale
- **Project type:** Telegram bot that proxies prompts to external LLM providers.
- **Tech stack:** Python 3, aiogram 3, httpx, environment-based configuration.
- **Key factor:** Small codebase and low domain complexity favor a simple structure with clear dependency flow.

## Folder Structure
```text
my_llm_bot/
├── bot/
│   ├── handlers/           # Presentation layer: Telegram commands and message handlers
│   ├── llm_clients/        # Integration layer: external LLM provider adapters
│   ├── config.py           # Configuration layer: environment loading and settings
│   ├── main.py             # Composition root and process startup
│   └── system_prompt.py    # Shared prompt constants used by handlers/clients
├── .ai-factory/            # AI context and architecture documentation
├── .env_example            # Example runtime configuration
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

## Dependency Rules
- `bot/main.py` may import configuration and handlers to assemble the application.
- `bot/handlers/` may import configuration, prompt constants, and LLM client registry.
- `bot/llm_clients/` may import configuration and shared base abstractions.
- `bot/config.py` should stay independent from Telegram and provider-specific runtime code.

- ✅ `handlers -> llm_clients`
- ✅ `handlers -> config`
- ✅ `llm_clients -> config`
- ❌ `config -> handlers`
- ❌ `config -> llm_clients`
- ❌ provider clients importing Telegram-specific code

## Layer Communication
- Telegram updates enter through `bot/handlers/main.py`.
- Handlers resolve the selected model and call an LLM client through its shared `ask()` interface.
- Provider clients translate internal prompt input into external HTTP API calls and return plain text responses.
- `bot/main.py` remains the only composition root that creates the bot and dispatcher.

## Key Principles
1. Keep Telegram-specific concerns inside handlers.
2. Keep provider-specific HTTP logic inside `bot/llm_clients/`.
3. Keep startup and wiring decisions in `bot/main.py`, not scattered across modules.

## Code Examples

### Handler Calls Integration Layer
```python
from aiogram import F, Router, types

from ..llm_clients import LLM_CLIENTS
from ..system_prompt import SYSTEM_PROMPT

router = Router()


@router.message(F.text)
async def chat_handler(message: types.Message):
    client = LLM_CLIENTS["gigachat"]
    response = await client.ask(message.text or "", SYSTEM_PROMPT)
    await message.answer(response)
```

### Provider Client Uses Shared Config
```python
import httpx

from ..config import settings


async def fetch_completion(payload: dict) -> dict:
    headers = {
        "Authorization": f"Api-Key {settings.yandex_api_key}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
    return response.json()
```

## Anti-Patterns
- ❌ Mixing Telegram update parsing with raw HTTP requests to providers inside the same handler branch.
- ❌ Spreading startup wiring across handlers or client modules instead of keeping it in `bot/main.py`.
- ❌ Introducing extra service/repository layers before the bot has real domain complexity that justifies them.
