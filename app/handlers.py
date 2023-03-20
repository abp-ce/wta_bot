import httpx
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from .config import settings
from .factories import ListCF
from .keyboards import get_list_kb, get_menu_kb
from .states import Task

router = Router()

BASE_URL = settings.backend_host


@router.message(Command(commands=["menu"]))
async def cmd_start(message: Message):
    name = message.chat.first_name
    await message.answer(f"Привет. {name}!", reply_markup=get_menu_kb())


@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    state.clear()
    await message.answer("Действие отменено")


@router.message(F.text == "По номеру")
async def by_no(message: Message, state: FSMContext):
    await message.answer("Введите номер задачи")
    await state.set_state(Task.no)


@router.message(F.text == "По названию")
async def by_name(message: Message, state: FSMContext):
    await message.answer("Введите название задачи, можно частично")
    await state.set_state(Task.name)


@router.message(F.text == "По сложности и категории")
async def by_level_and_theme(message: Message, state: FSMContext):
    jr = httpx.get(BASE_URL + "/levels").json()
    await message.answer(
        "Выберите сложность", reply_markup=get_list_kb(jr, "level")
    )
    await state.set_state(Task.level)


@router.callback_query(ListCF.filter(F.action == "level"))
async def get_levels(
    callback: CallbackQuery, callback_data: ListCF, state: FSMContext
):
    await state.update_data(level=callback_data.value)
    jr = httpx.get(BASE_URL + f"/themes/?level={callback_data.value}").json()
    await callback.message.answer(
        f"Выберите тему для уровня {callback_data.value}",
        reply_markup=get_list_kb(jr, "theme"),
    )
    await state.set_state(Task.theme)


async def get_tasks_by_url(url: str, message: Message, state: FSMContext):
    jr = httpx.get(url).json()
    text = (
        "Выберите для просмотра деталей"
        if jr
        else "К сожалению, ничего не нашлось"
    )
    mark_up = get_list_kb(jr, "name") if jr else None
    await message.answer(text, reply_markup=mark_up)
    await state.clear()


@router.callback_query(ListCF.filter(F.action == "theme"))
async def get_themes(
    callback: CallbackQuery, callback_data: ListCF, state: FSMContext
):
    data = await state.get_data()
    url = (
        BASE_URL
        + f"/list/?level={data['level']}&theme_id={callback_data.value}"
    )
    await get_tasks_by_url(url, callback.message, state)


@router.message(Task.no)
async def get_by_no(message: Message, state: FSMContext):
    url = BASE_URL + "/list/?no=" + message.text
    await get_tasks_by_url(url, message, state)


@router.message(Task.name)
async def get_by_name(message: Message, state: FSMContext):
    url = BASE_URL + "/list/?name=" + message.text
    await get_tasks_by_url(url, message, state)


@router.callback_query(ListCF.filter(F.action == "name"))
async def get_details(callback: CallbackQuery, callback_data: ListCF):
    url = BASE_URL + "/list/?" + "no=" + callback_data.value
    jr = httpx.get(url).json()[0]
    text = (
        f"Номер: {jr['no']}\nНазвание: {jr['name']}\n"
        f"Сложность: {jr['level']}\nРешений: {jr['solved']}\nТемы:\n"
    )
    url = BASE_URL + "/themes/" + callback_data.value
    jr = httpx.get(url).json()
    text += ", ".join([j["name"] for j in jr])
    await callback.message.answer(text=text)
