import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, LOGGER_PATH
from main_menu.handlers import main_menu_router

routers = [
    main_menu_router,
]


LOGGER_FORMAT = ("[%(asctime)s] %(levelname)s: %(message)s "
                 "(%(pathname)s:%(lineno)d)")
LOGGER_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


async def main() -> None:
    """Основная функция, которая инициализирует бота, настраивает логирование,
    подключает роутеры и запускает опрос бота. Использует асинхронное
    программирование.
    """
    bot_properties = DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN,
        link_preview_is_disabled=True
    )
    bot = Bot(
        token=BOT_TOKEN,
        default=bot_properties
    )
    dp = Dispatcher(storage=MemoryStorage())
    for router in routers:
        dp.include_routers(router)
    await bot.delete_webhook(drop_pending_updates=True)

    logging.basicConfig(
        level=logging.INFO,
        filename=LOGGER_PATH,
        format=LOGGER_FORMAT,
        datefmt=LOGGER_DATE_FORMAT
    )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
