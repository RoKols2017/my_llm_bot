import html

from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart

from ..system_prompt import SYSTEM_PROMPT
from ..config import settings
from ..llm_clients import LLM_CLIENTS, SUPPORTED_LLM_KEYS, get_available_llm_keys

router = Router()
user_model_preferences: dict[int, str] = {}


def _available_models_text() -> str:
    available = set(get_available_llm_keys())
    lines = []
    for key in SUPPORTED_LLM_KEYS:
        status = "доступна" if key in available else "не настроена"
        lines.append(f"- `{key}`: {status}")
    return "\n".join(lines)


def _resolve_model_key(user_id: int) -> str | None:
    preferred = user_model_preferences.get(user_id, settings.default_llm)
    if preferred in LLM_CLIENTS:
        return preferred

    available = get_available_llm_keys()
    if available:
        return available[0]
    return None

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Привет. Я Telegram-бот с поддержкой `gigachat` и `yandex`.\n\n"
        "Команды:\n"
        "- `/models` показать доступные модели\n"
        "- `/model gigachat` выбрать GigaChat\n"
        "- `/model yandex` выбрать YandexGPT"
    )


@router.message(Command("models"))
async def models_handler(message: types.Message):
    await message.answer(_available_models_text())


@router.message(Command("model"))
async def model_handler(message: types.Message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        current = _resolve_model_key(message.from_user.id) if message.from_user else None
        current_text = current or "не выбрана"
        await message.answer(
            "Укажи модель: `/model gigachat` или `/model yandex`.\n"
            f"Сейчас: `{current_text}`"
        )
        return

    llm_key = parts[1].strip().lower()
    if llm_key not in SUPPORTED_LLM_KEYS:
        await message.answer("Неизвестная модель. Доступны: `gigachat`, `yandex`.")
        return

    if llm_key not in LLM_CLIENTS:
        await message.answer(
            f"Модель `{llm_key}` не настроена в окружении.\n\n{_available_models_text()}"
        )
        return

    if message.from_user:
        user_model_preferences[message.from_user.id] = llm_key
    await message.answer(f"Активная модель: `{llm_key}`")


@router.message(F.text)
async def chat_handler(message: types.Message):
    user_prompt = message.text
    if not user_prompt or user_prompt.startswith("/"):
        return

    if not message.from_user:
        await message.answer("Не удалось определить пользователя Telegram.")
        return

    llm_key = _resolve_model_key(message.from_user.id)
    if not llm_key:
        await message.answer(
            "Нет ни одной настроенной модели. Проверь `.env` и добавь ключи для GigaChat или YandexGPT."
        )
        return

    client = LLM_CLIENTS[llm_key]

    await message.answer(f"Генерирую ответ через `{llm_key}`...")

    try:
        response = await client.ask(user_prompt, SYSTEM_PROMPT)
        await message.answer(response)
    except Exception as error:
        await message.answer(
            "Ошибка при обращении к модели. "
            f"Проверь ключи и параметры API.\n\n`{html.escape(str(error))}`"
        )
