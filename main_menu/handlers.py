import datetime
from typing import Union

from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.utils.payload import decode_payload

from app_tools.fitbit import get_auth_link, auth
from app_tools.server import get_user, update_verifyer_code, set_access_token, get_user_rating
from loggers import user_logger
from main_menu.constants import MainMenuMessage, MainMenuButton
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.markdown import hlink

from main_menu.keyboards import main_menu, back_main_menu

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
                MainMenuMessage.USER_AUTHORIZED_SUCCESSFULLY, reply_markup=main_menu()
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
            await message.answer(
                MainMenuMessage.RECOGNIZE_MESSAGE.format(user['name'] + ' ' + user['surname']), reply_markup=main_menu()
            )
        else:
            link, verifier = await get_auth_link()
            await message.answer(
                MainMenuMessage.START.format(hlink('ссылке', link)), parse_mode=ParseMode.HTML
            )
            await update_verifyer_code(message, verifier)

    await user_logger(message)


@main_menu_router.callback_query(F.data == MainMenuButton.ACCOUNT)
async def rating_handler(callback: types.CallbackQuery):
    user = await get_user(callback)

    message = 'Ваш аккаунт\n\nФИО:{}\nБЦ: {}\nВозраст: {}\nПол: {}\nНорма шагов на день: {}\nПроцент выполнения нормы шаго: {}%'

    formatted_message = message.format(
    ' '.join((user['name'], user['surname'], user['patronymic'])),
    user['bc'].replace('_', ' '),
    user['age'],
    user['sex'],
    user['step_norm_day'],
    int(100 * user['today_activity']/user['step_norm_day'])
    )

    await callback.message.answer(
        formatted_message,
        disable_web_page_preview=True,
        reply_markup=back_main_menu()
    )


@main_menu_router.callback_query(F.data == MainMenuButton.RATING)
async def rating_handler(callback: types.CallbackQuery):
    rating = await get_user_rating(callback.from_user.id)

    rating = rating['rating']

    message_template = 'Рейтинг за {}: \n{} ...\n\n Ваш рейтинг: {}'

    messages = [str(i[0]) + ': ' + ' '.join(i[1:-1]) + ': ' + str(i[-1]) for i in rating[:5]]

    main_rating = '\n'.join(messages)
    my_rating = str(rating[-1][0]) + ': ' + ' '.join(rating[-1][1:-1]) + ': ' + str(rating[-1][-1])

    message = message_template.format((datetime.date.today() - datetime.timedelta(days=1)).isoformat(), main_rating,
                                      my_rating)

    await callback.message.answer(
        message,
        disable_web_page_preview=True,
        reply_markup=back_main_menu()
    )


@main_menu_router.callback_query(F.data == MainMenuButton.BACK_TO_MAIN_MENU)
async def rating_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        'Главное меню',
        disable_web_page_preview=True,
        reply_markup=main_menu()
    )
