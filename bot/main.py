import asyncio
from aiogram import Bot, Dispatcher

from .config import settings
from .handlers import main as main_handlers


def _validate_settings() -> None:
    if not settings.bot_token:
        raise RuntimeError("Не задан BOT_TOKEN.")

    has_gigachat = bool(settings.gigachat_auth_key)
    has_yandex = bool(settings.yandex_api_key and (settings.yandex_folder_id or settings.yandex_model_uri))
    if not (has_gigachat or has_yandex):
        raise RuntimeError(
            "Нужно настроить хотя бы одну модель: GIGACHAT_AUTH_KEY или YANDEX_API_KEY с YANDEX_FOLDER_ID/YANDEX_MODEL_URI."
        )

async def main():
    _validate_settings()
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    dp.include_router(main_handlers.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
