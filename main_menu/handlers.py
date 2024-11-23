from typing import Union

from aiogram import Router, F, types

from loggers import user_logger
from main_menu.constants import MainMenuButton, \
    MainMenuMessage, SystemButton

main_menu_router = Router()


@main_menu_router.message(
    F.text == SystemButton.START
)
async def get_initial_message(message: types.Message) -> None:
    """Приветственное сообщение с инструкцией по работе с ботом"""
    await message.answer(
        MainMenuMessage.START
    )
    await user_logger(message)


