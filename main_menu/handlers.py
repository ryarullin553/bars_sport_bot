from typing import Union

from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.utils.payload import decode_payload

from app_tools.fitbit import get_auth_link, auth
from app_tools.server import get_user, update_verifyer_code, set_access_token
from loggers import user_logger
from main_menu.constants import MainMenuMessage
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.markdown import hlink

main_menu_router = Router()


@main_menu_router.message(CommandStart(deep_link=True))
async def get_code(message: types.Message, command: CommandObject):
    args = command.args

    if args:
        user = await get_user(message)
        access_data = await auth(args, user['code_verifier'])

        if access_data:
            await set_access_token(access_data, message.from_user.id)
            await message.answer(
                MainMenuMessage.USER_AUTHORIZED_SUCCESSFULLY
            )
            # menu()
        else:
            await message.answer(
                MainMenuMessage.USER_AUTHORIZED_UNSUCCESSFULLY
            )


@main_menu_router.message(CommandStart())
async def base_start(message: types.Message) -> None:
    """Приветственное сообщение с инструкцией по работе с ботом"""
    user = await get_user(message)

    if not user:
        await message.answer(
            MainMenuMessage.USER_NOT_FOUND
        )
    else:
        if user['fitbit_user_id']:
            # menu()
            pass
        else:
            link, verifier = await get_auth_link()
            await message.answer(
                MainMenuMessage.START.format(hlink('ссылке', link)), parse_mode=ParseMode.HTML
            )
            await update_verifyer_code(message, verifier)
#
#     await user_logger(message)
