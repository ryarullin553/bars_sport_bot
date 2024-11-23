from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import PROFESSIONAL_COMMUNITIES_URL, INTEREST_COMMUNITIES_URL
from main_menu.constants import MainMenuButton


def main_menu() -> InlineKeyboardMarkup:
    """Клавиатура отображающая кнопки главного меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.SERVICE,
            callback_data=MainMenuButton.SERVICE
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.BONUSES,
            callback_data=MainMenuButton.BONUSES
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.INFORMATIONAL_RESOURCES,
            callback_data=MainMenuButton.INFORMATIONAL_RESOURCES
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.COMMUNITIES_OF_INTEREST,
            callback_data=MainMenuButton.COMMUNITIES_OF_INTEREST
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=MainMenuButton.FAQ,
            callback_data=MainMenuButton.FAQ
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
