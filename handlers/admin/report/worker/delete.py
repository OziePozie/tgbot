from aiogram import Router
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


@router.callback_query(F.data.startswith('delete'))
async def workers_update(call: types.CallbackQuery, state: FSMContext):
    message_data = call.data.split('_')
    print(message_data)
    await call.message.edit_text("Выберите сотрудника",
                                 reply_markup=generate_employee_keyboard(WorkType.get_by_value(message_data[1])))
@router.callback_query(F.data.startswith('del_employee'))
async def employees_delete(call: types.CallbackQuery):
    message_data = call.data.split('_')
    id = message_data[2]
    employee = db_session.query(Workers).filter(Workers.id == id).first()
    keyboard = [
        [InlineKeyboardButton(text=f"Подтвердите удаление сотрудника \n"
                                   f"{employee.name}",
                              callback_data=f"d_{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="delete")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.edit_text("Выберите действие",
                                 reply_markup=markup)

@router.callback_query(F.data.startswith('d_'))
async def employees_delete_ok(call: types.CallbackQuery):
    message_data = call.data.split('_')
    id = message_data[1]
    employee = db_session.query(Workers).filter(Workers.id == id).delete()
    db_session.commit()
    keyboard = [
        [InlineKeyboardButton(text=f"Вернуться на главную", callback_data="back_main")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.edit_text("Успешное изменение. Выберите действие",
                                 reply_markup=markup)


def generate_employee_keyboard(worktype):
    markup = InlineKeyboardBuilder()
    employees = db_session.query(Workers.name, Workers.id).filter(Workers.work_type == worktype).all()
    print(employees)
    for employee_name, employee_id in employees:
        markup.button(
            text=f"{employee_name}",
            callback_data=f"del_employee_{employee_id}"
        )

    markup.button(text="Назад", callback_data="workers")
    markup.adjust(1)

    return markup.as_markup()


