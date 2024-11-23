from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import PROFESSIONAL_COMMUNITIES_URL, INTEREST_COMMUNITIES_URL
from main_menu.constants import MainMenuButton


def main_menu() -> InlineKeyboardMarkup:
    """Клавиатура отображающая кнопки главного меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.EVENTS,
            callback_data=MainMenuButton.EVENTS
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.RATING,
            callback_data=MainMenuButton.RATING
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.ACTIVITIES,
            callback_data=MainMenuButton.ACTIVITIES
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.ACCOUNT,
            callback_data=MainMenuButton.ACCOUNT
        )
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def keyboard_from_array(array: list, page: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for button in array:
        keyboard.add(
            InlineKeyboardButton(
                text=button[1],
                callback_data=button[0]
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=button[0]
        ),
        InlineKeyboardButton(
            text='Вперед',
            callback_data=button[0]
        ),
    )

    return keyboard.as_markup()



def communities_of_interest() -> InlineKeyboardMarkup:
    """Клавиатура показывающая кнопку 'Сообщества по интересам'"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.PROFESSIONAL_COMMUNITIES,
            url=PROFESSIONAL_COMMUNITIES_URL
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.INTEREST_COMMUNITIES,
            url=INTEREST_COMMUNITIES_URL
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.BACK_TO_MAIN_MENU,
            callback_data=MainMenuButton.BACK_TO_MAIN_MENU
        )
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def back_main_menu() -> InlineKeyboardMarkup:
    """Клавиатура показывающая кнопку 'Главное меню'"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.BACK_TO_MAIN_MENU,
            callback_data=MainMenuButton.BACK_TO_MAIN_MENU
        )
    )
    return keyboard.as_markup()
