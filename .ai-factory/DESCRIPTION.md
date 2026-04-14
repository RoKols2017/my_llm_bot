# Project: LLM Assistant Telegram Bot

## Overview
Telegram bot built with Python and aiogram 3 that routes user messages to one of two configured LLM providers: GigaChat or YandexGPT.

## Core Features
- Handle Telegram commands and free-form chat messages.
- Switch active model per user between `gigachat` and `yandex`.
- Validate runtime configuration before bot startup.
- Call external LLM APIs over HTTP and return generated responses to Telegram.

## Tech Stack
- **Language:** Python 3
- **Framework:** aiogram 3
- **Database:** None
- **ORM:** None
- **HTTP client:** httpx
- **Configuration:** python-dotenv + environment variables
- **Integrations:** Telegram Bot API, GigaChat API, YandexGPT API

## Architecture Notes
- Current codebase is intentionally small and uses a minimal module split: config, handlers, LLM clients, and startup entrypoint.
- User model preference is kept in process memory; there is no persistence layer.
- External providers are isolated in `bot/llm_clients/`, while Telegram-specific flow lives in `bot/handlers/`.

## Non-Functional Requirements
- Logging: not yet formalized in codebase.
- Error handling: fail fast on missing required config and surface provider errors back to the user.
- Security: secrets must stay in environment variables and never be committed.
- Testing: automated tests are not present yet; API verification currently depends on real credentials.

## Architecture
See `.ai-factory/ARCHITECTURE.md` for detailed architecture guidelines.
Pattern: Layered Architecture
