# LLM Assistant Telegram Bot

> Минималистичный Telegram-бот на `aiogram 3`, который отправляет запросы в `gigachat` или `yandex`.

Проект нужен для быстрого переключения между двумя LLM-провайдерами без лишней инфраструктуры. Бот валидирует конфигурацию на старте, хранит выбор модели в памяти и работает только через переменные окружения.

## Быстрый старт

```bash
pip install -r requirements.txt
cp .env_example .env
python -m bot.main
```

Подробная настройка переменных окружения и примеры `.env` вынесены в `docs/configuration.md`.

## Возможности

- **Два провайдера** - GigaChat и YandexGPT в одном боте.
- **Переключение модели** - пользователь может менять активную модель через Telegram-команду.
- **Минимальный runtime** - без базы данных, ORM и лишних слоев.
- **Проверка конфигурации** - бот не стартует с пустым `BOT_TOKEN` или без настроенного провайдера.

## Пример

```text
/models
- gigachat: доступна
- yandex: не настроена

/model gigachat
Активная модель: gigachat

Привет, что нового в ИИ?
Генерирую ответ через gigachat...
```

## Документация

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/getting-started.md) | Установка, запуск и первая проверка |
| [Configuration](docs/configuration.md) | Переменные окружения и примеры `.env` |
| [Architecture](docs/architecture.md) | Структура проекта и поток данных |
| [Deployment](docs/deployment.md) | Dockerfile, Compose и production overlay |

## License

MIT
