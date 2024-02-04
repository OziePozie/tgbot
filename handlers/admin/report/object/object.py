from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db_session
from data.models import Workers, WorkType, Object

router = Router()


@router.callback_query(F.data == 'object')
async def workers(call: types.CallbackQuery):
    keyboard = [
        [InlineKeyboardButton(text="Добавить", callback_data="object_add")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")]
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await call.message.edit_text("Выберите действие", reply_markup=markup)

class AddObject(StatesGroup):
    name = State()
    tg = State()

@router.callback_query(F.data == 'object_add')
async def object_add(call: types.CallbackQuery, state: FSMContext):

    message_data = call.data.split('_')

    print(message_data)

    await call.message.edit_text("Введите имя объекта")
    await state.set_state(AddObject.name)
    await call.message.delete()


@router.message(AddObject.name)
async def add_name_to_object(message: Message, state: FSMContext):
    print(message.text)
    await state.update_data(name=message.text)
    await state.set_state(AddObject.tg)
    await message.reply("Введите ссылку на ТГ группу объекта")

@router.message(AddObject.tg)
async def add_tg_to_object(message: Message, state: FSMContext):
    await state.update_data(tg=message.text)
    user_data = await state.get_data()
    object = Object(name=user_data['name'], tg_link=user_data['tg'])
    db_session.add(object)
    db_session.commit()
    keyboard = [
        [InlineKeyboardButton(text=f"Вернуться на главную", callback_data="back_main")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.reply(text="Успешное добавление. Выберите действие",
                        reply_markup=markup)


