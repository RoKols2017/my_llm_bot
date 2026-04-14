[← Getting Started](getting-started.md) · [Back to README](../README.md) · [Architecture →](architecture.md)

# Configuration

## Основная идея

Проект полностью настраивается через переменные окружения. Конфигурация загружается в `bot/config.py` через `python-dotenv`, а затем используется при старте и в клиентах провайдеров.

## Обязательные переменные

| Переменная | Обязательно | Назначение |
|------------|-------------|------------|
| `BOT_TOKEN` | Да | Токен Telegram-бота |
| `LLM_DEFAULT` | Нет | Модель по умолчанию: `gigachat` или `yandex` |

Нужно настроить хотя бы одного провайдера: GigaChat или YandexGPT.

## GigaChat

| Переменная | Обязательно | Значение по умолчанию | Назначение |
|------------|-------------|-----------------------|------------|
| `GIGACHAT_AUTH_KEY` | Да, если используете GigaChat | - | Basic auth key для OAuth |
| `GIGACHAT_SCOPE` | Нет | `GIGACHAT_API_PERS` | Scope для получения токена |
| `GIGACHAT_MODEL` | Нет | `GigaChat` | Имя модели для chat completions |

Пример:

```env
BOT_TOKEN=telegram-token
LLM_DEFAULT=gigachat
GIGACHAT_AUTH_KEY=basic-auth-key
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_MODEL=GigaChat
```

## YandexGPT

| Переменная | Обязательно | Значение по умолчанию | Назначение |
|------------|-------------|-----------------------|------------|
| `YANDEX_API_KEY` | Да, если используете YandexGPT | - | API key Yandex Cloud |
| `YANDEX_FOLDER_ID` | Да, если не задан `YANDEX_MODEL_URI` | - | Folder ID для сборки `modelUri` |
| `YANDEX_MODEL_URI` | Нет | - | Полный URI модели, если нужен явный выбор |

Пример:

```env
BOT_TOKEN=telegram-token
LLM_DEFAULT=yandex
YANDEX_API_KEY=yandex-api-key
YANDEX_FOLDER_ID=folder-id
```

Если нужен явный URI:

```env
YANDEX_MODEL_URI=gpt://folder-id/yandexgpt-lite/latest
```

## Проверка конфигурации при старте

В `bot/main.py` приложение проверяет:

- задан ли `BOT_TOKEN`
- настроен ли хотя бы один провайдер
- есть ли у YandexGPT либо `YANDEX_FOLDER_ID`, либо `YANDEX_MODEL_URI`

Если проверка не проходит, бот завершается сразу, не начиная polling.

## Безопасность

- Не коммитьте реальный `.env`.
- Не публикуйте API-ключи в логах и скриншотах.
- Для MCP GitHub в `.mcp.json` нужен `GITHUB_TOKEN`, если вы захотите использовать GitHub server.

## See Also

- [Getting Started](getting-started.md) - установка, запуск и базовая проверка
- [Architecture](architecture.md) - где именно используется конфигурация в коде
