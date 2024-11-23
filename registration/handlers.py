import json

import aiohttp.web
from aiogram import Router, F, types
from aiogram.enums import ParseMode

import http_sessions
from config import TELEGRAM_REGISTER_URL, INTEGRATOR_LOGIN, \
    INTEGRATOR_PASSWORD, GET_ACCOUNT_URL
from loggers import user_logger, error_logger
from main_menu.constants import ErrorMessage, MainMenuMessage
from main_menu.keyboards import main_menu, registration
from registration.constants import RegistrationMessage, RegistrationButton
from registration.keyboards import send_contacts, get_bo_account
from registration.tools import convert_message_to_correct_format

registration_router = Router()


@registration_router.callback_query(F.data == RegistrationButton.NEW_USER)
async def get_button_registry_tg_account(callback: types.CallbackQuery) -> None:
    """Передача кнопки вызова сохранения телеграм-аккаунта в БО"""
    await callback.message.answer(
        RegistrationMessage.SEND_CONTACT,
        disable_web_page_preview=True,
        reply_markup=send_contacts(),
    )
    await user_logger(callback)


@registration_router.message(F.contact)
async def telegram_account_registry(message: types.Message) -> None:
    """Функция регистрации аккаунта в боте.

    Args:
        message (types.Message): Объект сообщения пользователя.

    1. Извлекает данные о пользователе из сообщения.
    2. Формирует словарь с данными пользователя.
    3. Отправляет запрос на регистрацию аккаунта Telegram.
    4. Обрабатывает ответ:
        - Если успешно зарегистрирован:
        - Если пользователь уже существует, отправляет сообщение
        "Привязка завершена" и клавиатуру "Главное меню".
        - Если кандидат уже существует, отправляет сообщение
        "Привязка завершена" и клавиатуру "Получение учетной записи".
        - Если аккаунт не найден, отправляет сообщение
        "Учетная запись не найдена" и клавиатуру "Отправить контактные данные".
        - Если произошла ошибка, отправляет сообщение "Сообщение не доставлено"
        и убирает клавиатуру.
    5. Если данные пользователя некорректны, отправляет сообщение
    "Некорректный ввод данных" и клавиатуру "Отправить контактные данные".
    6. Логгирует действия пользователя.
    """
    user_id: int = message.contact.user_id
    phone: str = message.contact.phone_number
    chat_id: int = message.chat.id
    data = {
        "phone": phone,
        "user_id": user_id,
        "chat_id": chat_id,
        "login_integrator": INTEGRATOR_LOGIN,
        "password_integrator": INTEGRATOR_PASSWORD
    }
    if user_id == message.from_user.id:
        try:
            response = await http_sessions.post(
                TELEGRAM_REGISTER_URL,
                data=data
            )
            response_data = json.loads(response)
            extra_params = response_data.get("extra", {})
            user_exist = extra_params.get("tg_user_exist")
            candidat_exist = extra_params.get("candidat_exist")
            success = response_data.get("success")
            if success:
                if user_exist:
                    answer_message = RegistrationMessage.BINDING_ACCOUNT_SAVE
                    keyboard = types.ReplyKeyboardRemove()
                else:
                    if candidat_exist:
                        answer_message = \
                            RegistrationMessage.BINDING_ACCOUNT_SAVE
                        keyboard = get_bo_account()
                    else:
                        answer_message = ErrorMessage.ACCOUNT_NOT_FOUND
                        keyboard = send_contacts()
            else:
                answer_message = ErrorMessage.UNKNOWN_EMPLOYEE
                keyboard = send_contacts()
            await message.answer(
                answer_message,
                reply_markup=keyboard
            )
            if answer_message == RegistrationMessage.BINDING_ACCOUNT_SAVE:
                await message.answer(
                    MainMenuMessage.START,
                    reply_markup=main_menu()
                )
        except aiohttp.ClientError as error:
            await error_logger(message, error)
            await message.answer(
                ErrorMessage.MESSAGE_NOT_SEND,
                reply_markup=registration()
            )
    else:
        await message.answer(
            ErrorMessage.INCORRECT_INPUT,
            reply_markup=send_contacts()
        )
    await user_logger(message)


@registration_router.message(F.text == RegistrationButton.GET_BO_ACCOUNT)
async def send_get_account(message: types.Message) -> None:
    """Функция отправляет запрос на получение учетной записи пользователя
    и обрабатывает полученный ответ.

    Args:
        message (types.Message): Объект сообщения пользователя.
    """
    from_user_id: int = message.from_user.id
    payload = {
        "user_id": from_user_id,
        "login_integrator": INTEGRATOR_LOGIN,
        "password_integrator": INTEGRATOR_PASSWORD,
    }
    response = await http_sessions.post(
        GET_ACCOUNT_URL,
        data=payload
    )
    response_data = json.loads(response)
    success = response_data.get("success")
    extra_data = response_data.get("extra", {})
    candidate_exist = extra_data.get("candidate_exist")
    freshman_messages = extra_data.get("freshman_messages")

    if success:
        if candidate_exist:
            answer_message = response_data.get("message", "")
        else:
            answer_message = ErrorMessage.ACCOUNT_NOT_FOUND
        await message.answer(
            answer_message,
            reply_markup=types.ReplyKeyboardRemove()
        )

        if freshman_messages:
            for freshman_message in freshman_messages:
                await message.answer(
                    convert_message_to_correct_format(freshman_message),
                    parse_mode=ParseMode.HTML,
                    reply_markup=types.ReplyKeyboardRemove()
                )
    else:
        await message.answer(
            ErrorMessage.NOT_BARS_OFFICE,
            reply_markup=types.ReplyKeyboardRemove()
        )
    await user_logger(message)
