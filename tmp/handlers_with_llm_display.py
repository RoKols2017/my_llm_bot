import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.chat_action import ChatActionSender
from bot.llm_clients import LLM_CLIENTS
from bot.config import settings

router = Router()

@router.message(CommandStart())
async def cmd_start(msg: Message) -> None:
    current_llm = settings.llm_default
    await msg.answer(f"👋 Привет! Я бот. Сейчас я использую <b>{current_llm}</b> как LLM.")

@router.message()
async def handle_message(msg: Message) -> None:
    async with ChatActionSender.typing(chat_id=msg.chat.id, bot=msg.bot):
        llm_class = LLM_CLIENTS.get(settings.llm_default)
        if llm_class is None:
            await msg.answer("❌ Ошибка: выбранная LLM не реализована.")
            return
        client = llm_class()
        reply = await asyncio.to_thread(client.ask, msg.text)
    await msg.answer(f"🤖 <b>[{settings.llm_default}]</b>: {reply}")
