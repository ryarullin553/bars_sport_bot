from aiogram import types


async def user_not_found(message: types.Message):
    await message.answer(
        'Пользователь не найден'
    )


def format_event(event):
    return (
        f"📅 <b>{event['name']}</b>\n"
        f"🔹 Период: {event['date_start']} - {event['date_end']}\n"
        f"🎯 Цель: {event['goal']}\n"
        f"📊 Баллы: {event['all_points']}\n"
        f"📈 Индикатор: {event['indicator__name']}\n"
        f"ID: {event['id']}\n"
    )


def format_activity(event):
    return (
        f"🏋️ <b>{event['name']}</b>\n"
        f"📍 Город: {event['town']}\n"
        f"📅 Дата начала: {event['date_start']}\n"
        f"🆔 ID мероприятия: {event['id']}"
    )