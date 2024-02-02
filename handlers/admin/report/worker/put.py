from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db_session
from data.models import Workers, WorkType

router = Router()


@router.callback_query(F.data.startswith('put'))
async def workers_update(call: types.CallbackQuery, state: FSMContext):
    message_data = call.data.split('_')
    print(message_data)
    await call.message.edit_text("Выберите сотрудника",
                                 reply_markup=generate_employee_keyboard())


@router.callback_query(F.data.startswith('update_employee'))
async def employees_update(call: types.CallbackQuery):
    message_data = call.data.split('_')
    id = message_data[2]
    keyboard = [
        [InlineKeyboardButton(text="ФИО", callback_data=f"update_fio_{id}")],
        [InlineKeyboardButton(text="Профессия", callback_data=f"update_profession_{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="put")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.edit_text("Выберите что изменить",
                                 reply_markup=markup)


class FioUpdate(StatesGroup):
    name = State()
    id = State()


@router.callback_query(F.data.startswith('update_fio'))
async def fio_update(call: types.CallbackQuery, state: FSMContext):
    message_data = call.data.split('_')
    id = message_data[2]
    await state.update_data(id=id)
    await call.message.edit_text("Введите Ф.И.О")
    await state.set_state(FioUpdate.name)


@router.message(FioUpdate.name)
async def fio_update_state(message: Message, state: FSMContext):
    user_data = await state.get_data()
    worker = (db_session.query(Workers)
              .filter(Workers.id == user_data['id'])
              .first())
    worker.name = message.text
    db_session.commit()
    await message.edit_text("Успешное изменение")


@router.callback_query(F.data.startswith('update_profession'))
async def profession_update(call: types.CallbackQuery, state: FSMContext):
    message_data = call.data.split('_')
    id = message_data[2]
    keyboard = [
        [InlineKeyboardButton(text="Мастера", callback_data=f"profession_master_{id}")],
        [InlineKeyboardButton(text="Электромонтеры", callback_data=f"profession_electrician_{id}")],
        [InlineKeyboardButton(text="Испытатели", callback_data=f"profession_tester_{id}")],
        [InlineKeyboardButton(text="АУР (ИТР)", callback_data=f"profession_aur_{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="put")]
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.edit_text("Выберите новую профессию",
                                 reply_markup=markup)


@router.callback_query(F.data.startswith('profession'))
async def profession_update_state(call: types.CallbackQuery):
    callback_data = call.data.split('_')
    worker = db_session.query(Workers).filter(Workers.id == callback_data[2]).first()
    worker.work_type = WorkType.get_by_value(callback_data[1])
    db_session.commit()
    await call.message.edit_text("Успешное изменение")


def generate_employee_keyboard():
    markup = InlineKeyboardBuilder()
    employees = db_session.query(Workers.name, Workers.id).all()
    print(employees)
    for employee_name, employee_id in employees:
        markup.button(
            text=f"{employee_name}",
            callback_data=f"update_employee_{employee_id}"
        )

    markup.button(text="Назад", callback_data="workers")
    markup.adjust(1)

    return markup.as_markup()
