from aiogram import Router, types, F
from aiogram.filters import CommandStart
from ..system_prompt import SYSTEM_PROMPT
from ..llm_clients import LLM_CLIENTS
from ..config import LLM_DEFAULT

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет! Я твой персональный LLM-ассистент. "
        "Задай вопрос — и я подключу одну из лучших языковых моделей!"
    )

@router.message(F.text)
async def chat_handler(message: types.Message):
    user_prompt = message.text
    llm_key = LLM_DEFAULT

    # Можно добавить выбор LLM по команде/настройке пользователя
    client = LLM_CLIENTS.get(llm_key)
    if not client:
        await message.answer("Сорри, что-то пошло не так с выбором модели.")
        return

    await message.answer("Генерирую ответ... 🤔")

    try:
        response = await client.ask(user_prompt, SYSTEM_PROMPT)
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Что-то пошло не так: {e}")
