from aiogram import types


async def user_not_found(message: types.Message):
    await message.answer(
        'Пользователь не найден'
    )
