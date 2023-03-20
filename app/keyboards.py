from typing import List

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .factories import ListCF


def get_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="По номеру")
    kb.button(text="По названию")
    kb.button(text="По сложности и категории")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_list_kb(items: List[dict], action: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    adjust = 1
    for it in items:
        if action == "name":
            text = f'{it["no"]} {it["name"]}'
            value = it["no"]
        elif action == "level":
            text = str(it) if it else "Пусто"
            value = it
            adjust = 6
        else:
            text = it["name"]
            value = it["id"]
        kb.button(
            text=text,
            callback_data=ListCF(value=value, action=action),
            adjust=2,
        )
    kb.adjust(adjust)
    return kb.as_markup()
