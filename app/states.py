from aiogram.fsm.state import State, StatesGroup


class Task(StatesGroup):
    no = State()
    name = State()
    level = State()
    theme = State()
