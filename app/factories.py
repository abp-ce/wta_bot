from aiogram.filters.callback_data import CallbackData


class ListCF(CallbackData, prefix="list"):
    action: str
    value: str
