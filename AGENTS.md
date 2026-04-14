# AGENTS.md

> Project map for AI agents. Keep this file up-to-date as the project evolves.

## Project Overview
Small Telegram bot that proxies user prompts to GigaChat or YandexGPT. The project is intentionally minimal and relies on environment-based configuration.

## Tech Stack
- **Language:** Python 3
- **Framework:** aiogram 3
- **Database:** None
- **ORM:** None

## Project Structure
```text
my_llm_bot/
├── bot/                    # Application package
│   ├── handlers/           # Telegram command and message handlers
│   ├── llm_clients/        # Provider-specific LLM API clients
│   ├── config.py           # Environment loading and settings object
│   ├── main.py             # Bot startup and configuration validation
│   └── system_prompt.py    # Shared system prompt sent to providers
├── .ai-factory/            # AI project context files
├── deploy/scripts/         # Helper scripts for container deployment and ops
├── docs/                   # Detailed project documentation
├── .env_example            # Example environment variables
├── .dockerignore           # Docker build context exclusions
├── Dockerfile              # Multi-stage image for development and production
├── compose.yml             # Base Docker Compose configuration
├── compose.override.yml    # Development Docker overrides
├── compose.production.yml  # Hardened production Docker overlay
├── requirements.txt        # Python dependencies
├── README.md               # Project overview and setup guide
└── .mcp.json               # Project MCP server configuration
```

## Key Entry Points
| File | Purpose |
|------|---------|
| `bot/main.py` | Composition root: validates settings, creates bot and dispatcher, starts polling |
| `bot/handlers/main.py` | Telegram router with `/start`, `/models`, `/model`, and chat message handling |
| `bot/config.py` | Loads environment variables into immutable settings |
| `bot/llm_clients/gigachat.py` | GigaChat OAuth and chat completion client |
| `bot/llm_clients/yandex.py` | YandexGPT completion client |
| `Dockerfile` | Multi-stage container build definition |
| `compose.yml` | Base container orchestration file |
| `.env_example` | Documents required runtime configuration |

## Documentation
| Document | Path | Description |
|----------|------|-------------|
| README | `README.md` | Project landing page |
| Getting Started | `docs/getting-started.md` | Installation, setup, first steps |
| Configuration | `docs/configuration.md` | Environment variables and examples |
| Architecture | `docs/architecture.md` | Project structure and data flow |
| Deployment | `docs/deployment.md` | Docker and Compose workflow |

## AI Context Files
| File | Purpose |
|------|---------|
| `AGENTS.md` | This file - project structure map |
| `.ai-factory/DESCRIPTION.md` | Project specification and tech stack |
| `.ai-factory/ARCHITECTURE.md` | Architecture decisions and guidelines |

## Notes
- There is no persistence layer; user model choice is stored in memory.
- Real provider verification requires valid API credentials in `.env`.
