# LLM Assistant Telegram Bot

Telegram-бот на `aiogram 3`, который умеет работать с двумя провайдерами:

- `gigachat`
- `yandex`

Старые заглушки и `ProxyAPI` удалены. В репозитории осталась только рабочая интеграция с GigaChat и YandexGPT.

## Что изменилось по API

- `GigaChat`: актуальная схема авторизации теперь строится через `POST /api/v2/oauth`, после чего запросы идут с `Bearer` токеном в `POST /api/v1/chat/completions`.
- `YandexGPT`: документация уехала в `AI Studio`, но для серверной интеграции бот использует рабочий REST-запрос с `Api-Key`, `modelUri` и `messages`.

## Возможности

- Выбор модели через команды Telegram.
- Отдельная настройка GigaChat и YandexGPT через `.env`.
- Нормальная проверка конфигурации при старте.
- Минимальная архитектура без лишних абстракций.

## Структура

```text
my_llm_bot/
├── bot/
│   ├── config.py
│   ├── handlers/
│   │   └── main.py
│   ├── llm_clients/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── gigachat.py
│   │   └── yandex.py
│   ├── main.py
│   └── system_prompt.py
├── .env_example
├── requirements.txt
└── README.md
```

## Быстрый старт

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Создайте `.env`:

```bash
cp .env_example .env
```

3. Заполните переменные окружения.

Минимум для GigaChat:

```env
BOT_TOKEN=your_telegram_bot_token_here
LLM_DEFAULT=gigachat

GIGACHAT_AUTH_KEY=your_gigachat_basic_auth_key_here
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_MODEL=GigaChat
```

Минимум для YandexGPT:

```env
BOT_TOKEN=your_telegram_bot_token_here
LLM_DEFAULT=yandex

YANDEX_API_KEY=your_yandex_api_key_here
YANDEX_FOLDER_ID=your_yandex_folder_id_here
```

Если нужен явный URI модели YandexGPT:

```env
YANDEX_MODEL_URI=gpt://<folder_id>/yandexgpt-lite/latest
```

4. Запустите бота:

```bash
python -m bot.main
```

## Команды в Telegram

- `/start` показать справку
- `/models` показать, какие модели настроены
- `/model gigachat` переключиться на GigaChat
- `/model yandex` переключиться на YandexGPT

## Переменные окружения

- `BOT_TOKEN` - токен Telegram-бота
- `LLM_DEFAULT` - модель по умолчанию: `gigachat` или `yandex`
- `GIGACHAT_AUTH_KEY` - basic auth key из кабинета GigaChat API
- `GIGACHAT_SCOPE` - обычно `GIGACHAT_API_PERS`
- `GIGACHAT_MODEL` - имя модели GigaChat, по умолчанию `GigaChat`
- `YANDEX_API_KEY` - API key Yandex Cloud
- `YANDEX_FOLDER_ID` - folder ID для `modelUri`
- `YANDEX_MODEL_URI` - необязательный полный URI модели YandexGPT

## Ограничения

- Переключение модели хранится в памяти процесса, без базы данных.
- Автотестов в проекте пока нет.
- Проверка реальных API-вызовов требует рабочих ключей в `.env`.

## Безопасность

Не коммитьте реальный `.env` и реальные API-ключи.
