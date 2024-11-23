import datetime
from typing import Union

from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.payload import decode_payload

from app_tools.fitbit import get_auth_link, auth
from app_tools.server import get_user, update_verifyer_code, set_access_token, get_user_rating, get_events, \
    get_my_events, add_to_event, get_my_activities, add_to_activities, get_activities
from app_tools.telegram import format_event, format_activity
from loggers import user_logger
from main_menu.constants import MainMenuMessage, MainMenuButton
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.markdown import hlink

from main_menu.keyboards import main_menu, back_main_menu, events_menu

main_menu_router = Router()
class CustomCallback(CallbackData, prefix="event"):
    id: str
    name: str
    type: str


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


@main_menu_router.callback_query(F.data == MainMenuButton.EVENTS)
async def main_event_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        "Меню мероприятий.",
        disable_web_page_preview=True,
        reply_markup=events_menu()
    )


@main_menu_router.callback_query(F.data == MainMenuButton.EVENTS_ALL)
async def event_handler(callback: types.CallbackQuery):
    events = await get_events(callback.from_user.id)

    message = 'Все Командные активности:'

    if not events:
        await callback.message.answer(
            "Мероприятий пока нет.",
            disable_web_page_preview=True,
            reply_markup=back_main_menu()
        )
    else:
        await callback.message.answer(
            message,
            disable_web_page_preview=True
        )
        for event in events[:-1]:
            keyboard = InlineKeyboardBuilder()
            keyboard.add(InlineKeyboardButton(text='Записаться',
                                              callback_data=CustomCallback(type='event', id=event['id'],
                                                                           name=event['name']).pack()))
            await callback.message.answer(
                format_event(event),
                disable_web_page_preview=True,
                reply_markup=keyboard.as_markup(),
                parse_mode=ParseMode.HTML
            )

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='Записаться',
                                          callback_data=CustomCallback(id=events[-1]['id'],
                                                                       name=events[-1]['name'], type='event').pack()))
        keyboard.add(
            InlineKeyboardButton(
                text=MainMenuButton.BACK_TO_MAIN_MENU,
                callback_data=MainMenuButton.BACK_TO_MAIN_MENU
            )
        )
        await callback.message.answer(
            format_event(events[-1]),
            disable_web_page_preview=True,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )


@main_menu_router.callback_query(F.data == MainMenuButton.EVENTS_ALL)
async def my_event_handler(callback: types.CallbackQuery):
    events = await get_my_events(callback.from_user.id)

    message = 'Все мои активности:'

    if not events:
        await callback.message.answer(
            "Вы не участвуете в мероприятиях.",
            disable_web_page_preview=True,
            reply_markup=back_main_menu()
        )
    else:
        await callback.message.answer(
            message,
            disable_web_page_preview=True
        )
        for event in events[:-1]:
            await callback.message.answer(
                format_event(event),
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML
            )

        await callback.message.answer(
            format_event(events[-1]),
            disable_web_page_preview=True,
            reply_markup=back_main_menu(),
            parse_mode=ParseMode.HTML
        )


@main_menu_router.callback_query(CustomCallback.filter(F.type == 'event'))
async def event_sign_up(callback: types.CallbackQuery, callback_data: CustomCallback):
    result = await add_to_event(callback.from_user.id, callback_data.id)

    if result:
        await callback.message.answer(
            'Вы успешно записались на мероприятие',
            reply_markup=back_main_menu()
        )
    else:
        await callback.message.answer(
            'Вы не можете записаться на это мероприятие',
            reply_markup=back_main_menu()
        )


@main_menu_router.callback_query(F.data == MainMenuButton.ACTIVITIES)
async def main_activity_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        "Меню Активностей.",
        disable_web_page_preview=True,
        reply_markup=events_menu()
    )


@main_menu_router.callback_query(F.data == MainMenuButton.ACTIVITIES_ALL)
async def activity_handler(callback: types.CallbackQuery):
    events = await get_activities(callback.from_user.id)

    message = 'Все тренировки:'

    if not events:
        await callback.message.answer(
            "Тренировок пока нет.",
            disable_web_page_preview=True,
            reply_markup=back_main_menu()
        )
    else:
        await callback.message.answer(
            message,
            disable_web_page_preview=True
        )
        for event in events[:-1]:
            keyboard = InlineKeyboardBuilder()
            keyboard.add(InlineKeyboardButton(text='Записаться',
                                              callback_data=CustomCallback(type='activity', id=event['id'],
                                                                           name=event['name']).pack()))
            await callback.message.answer(
                format_activity(event),
                disable_web_page_preview=True,
                reply_markup=keyboard.as_markup(),
                parse_mode=ParseMode.HTML
            )

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text='Записаться',
                                          callback_data=CustomCallback(id=events[-1]['id'],
                                                                       name=events[-1]['name'], type='activity').pack()))
        keyboard.add(
            InlineKeyboardButton(
                text=MainMenuButton.BACK_TO_MAIN_MENU,
                callback_data=MainMenuButton.BACK_TO_MAIN_MENU
            )
        )
        await callback.message.answer(
            format_activity(events[-1]),
            disable_web_page_preview=True,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.HTML
        )


@main_menu_router.callback_query(F.data == MainMenuButton.ACTIVITIES_ALL)
async def my_activity_handler(callback: types.CallbackQuery):
    events = await get_my_activities(callback.from_user.id)

    message = 'Все мои тренировки:'

    if not events:
        await callback.message.answer(
            "Вы не участвуете в тренировках.",
            disable_web_page_preview=True,
            reply_markup=back_main_menu()
        )
    else:
        await callback.message.answer(
            message,
            disable_web_page_preview=True
        )
        for event in events[:-1]:
            await callback.message.answer(
                format_activity(event),
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML
            )

        await callback.message.answer(
            format_activity(events[-1]),
            disable_web_page_preview=True,
            reply_markup=back_main_menu(),
            parse_mode=ParseMode.HTML
        )


@main_menu_router.callback_query(CustomCallback.filter(F.type == 'activity'))
async def activity_sign_up(callback: types.CallbackQuery, callback_data: CustomCallback):
    result = await add_to_activities(callback.from_user.id, callback_data.id)

    if result:
        await callback.message.answer(
            'Вы успешно записались на тренировку',
            reply_markup=back_main_menu()
        )
    else:
        await callback.message.answer(
            'Вы не можете записаться на это тренировку',
            reply_markup=back_main_menu()
        )


@main_menu_router.callback_query(F.data == MainMenuButton.ACCOUNT)
async def account_handler(callback: types.CallbackQuery):
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
