[← Architecture](architecture.md) · [Back to README](../README.md)

# Deployment

## Что добавлено

В проекте есть минимальный Docker-набор для stateless Telegram-бота:

| Файл | Назначение |
|------|------------|
| `Dockerfile` | Multi-stage образ с `development` и `production` stage |
| `compose.yml` | Базовый Compose-файл с общим сервисом `app` |
| `compose.override.yml` | Dev-override со сборкой и bind mount исходников |
| `compose.production.yml` | Hardened overlay для production-запуска |
| `.dockerignore` | Исключения для build context |
| `deploy/scripts/` | Скрипты deploy, update, logs, health-check, rollback |

## Локальная разработка через Docker

1. Создайте `.env` из `.env_example`.
2. Соберите и запустите контейнер:

```bash
cp .env_example .env
docker compose up --build
```

По умолчанию `compose.override.yml` использует stage `development` и монтирует проект в `/app`.

## Production overlay

Для production используется предсобранный образ, а не локальная сборка внутри overlay:

```bash
docker build --target production -t my-llm-bot:local .
APP_IMAGE=my-llm-bot:local docker compose -f compose.yml -f compose.production.yml up -d
```

## Hardening в production

- `read_only: true`
- `no-new-privileges:true`
- `cap_drop: [ALL]`
- запуск от `user: "1001:1001"`
- `tmpfs` для `/tmp`
- healthcheck на импорт `bot.main`
- log rotation через `json-file`
- resource limits в `deploy.resources`

## Скрипты

| Скрипт | Назначение |
|--------|------------|
| `deploy/scripts/deploy.sh` | Подтянуть образ и поднять production stack |
| `deploy/scripts/update.sh` | Выполнить update с health-check после перезапуска |
| `deploy/scripts/logs.sh` | Смотреть логи контейнера `app` |
| `deploy/scripts/health-check.sh` | Проверить контейнер и импорт `bot.main` |
| `deploy/scripts/rollback.sh` | Поднять предыдущий тег образа |
| `deploy/scripts/backup.sh` | Сейчас no-op, потому что stateful сервисов нет |

## Ограничения

- HTTP-портов нет, потому что это Telegram-бот, а не веб-сервис.
- Healthcheck проверяет импорт приложения, а не внешний endpoint.
- Для production нужен подготовленный `.env` и заранее собранный или опубликованный образ.

## See Also

- [Getting Started](getting-started.md) - локальный запуск без Docker
- [Configuration](configuration.md) - все runtime-переменные окружения
- [Architecture](architecture.md) - где находятся слои приложения
