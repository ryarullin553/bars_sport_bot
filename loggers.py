import logging
from typing import Union

from aiogram import types


async def user_logger(message: Union[types.Message, types.CallbackQuery]):
    """Логгирование информации о пользователе.

    Args:
        message (Union[types.Message, types.CallbackQuery]):
        Объект сообщения, содержащий информацию о пользователе и текст.
    """
    user_id: int = message.from_user.id
    username: str = message.from_user.username
    try:
        text: str = message.text
    except AttributeError:
        text = message.data
    logging.info(f"user_id: {user_id} (@{username}) - {text}")


async def error_logger(message: Union[types.Message, types.CallbackQuery], error):
    """Логгирование ошибок.

    Args:
        message (Union[types.Message, types.CallbackQuery]):
        Объект сообщения, содержащий информацию о пользователе и текст.
        error (str): Ошибка, вызвавшая логгирование.
    """
    user_id: int = message.from_user.id
    username: str = message.from_user.username
    try:
        text: str = message.text
    except AttributeError:
        text = message.data
    logging.error(f"user_id: {user_id} (@{username}) - {text} - {error}")
