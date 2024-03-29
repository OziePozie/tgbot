from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from context.admin.login import AdminLogin
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db_session, admin_login, admin_password
from data.models import Workers, WorkType
from handlers.admin.report.report import report_router
from handlers.admin.list.list import router as list_router

router = Router()
router.include_router(report_router)
router.include_router(list_router)


def main():
    keyboard = [
        [InlineKeyboardButton(text="Сформировать список", callback_data="report")],
        [InlineKeyboardButton(text="Отчет по объекту", callback_data='list')],

    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


@router.message(Command('admin'))
async def admin(message: types.Message, state: FSMContext):
    await message.answer("Логин:")
    await state.set_state(AdminLogin.login)


@router.message(AdminLogin.login)
async def set_login(message: types.Message, state: FSMContext):
    if message.text in admin_login:
        await message.answer("Пароль:")
        await state.set_state(AdminLogin.password)


@router.message(lambda message: message.text is not admin_login, AdminLogin.login)
async def log_pass_invalid(message: types.Message):
    await message.answer("Неверный логин")


@router.message(AdminLogin.password)
async def set_password(message: types.Message, state: FSMContext):
    if message.text in admin_password:
        await message.answer("Добро пожаловать", reply_markup=main())
        await state.clear()


@router.message(lambda message: message.text is not admin_password, AdminLogin.password)
async def _password(message: types.Message):
    await message.answer("Неверный пароль")


@router.callback_query(F.data == "back_main")
async def back_main(call: types.CallbackQuery):
    await call.message.edit_text("Добро пожаловать", reply_markup=main())


@router.callback_query(F.data == 'report')
async def report(call: types.CallbackQuery):
    keyboard = [
        [InlineKeyboardButton(text="Персонал", callback_data="workers")],
        [InlineKeyboardButton(text="Объект", callback_data="object")],
        [InlineKeyboardButton(text="Авто", callback_data="auto")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await call.message.edit_text("Выберите действие", reply_markup=markup)


# @router.callback_query(F.data == 'list')
# async def list(call: types.CallbackQuery):
#     keyboard = [
#         [InlineKeyboardButton(text="Выбор объекта", callback_data="choice_object")],
#         [InlineKeyboardButton(text="Назад", callback_data="back_main")]]
#
#     markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
#
#     await call.message.edit_text("Выберите объект", reply_markup=markup)


@router.callback_query(F.data == 'workers')
async def workers(call: types.CallbackQuery):
    keyboard = [
        [InlineKeyboardButton(text="Добавить", callback_data="add")],
        [InlineKeyboardButton(text="Изменить", callback_data="put")],
        [InlineKeyboardButton(text="Удалить", callback_data="delete")],
        [InlineKeyboardButton(text="Назад", callback_data="report")]
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await call.message.edit_text("Выберите действие", reply_markup=markup)


@router.callback_query(F.data == 'add')
async def workers_type_add(call: types.CallbackQuery, state: FSMContext):
    keyboard = [
        [InlineKeyboardButton(text="Мастера", callback_data="add_master")],
        [InlineKeyboardButton(text="Электромонтеры", callback_data="add_electrician")],
        [InlineKeyboardButton(text="Испытатели", callback_data="add_tester")],
        [InlineKeyboardButton(text="АУР (ИТР)", callback_data="add_aur")],
        [InlineKeyboardButton(text="Назад", callback_data="workers")]
    ]
    await state.set_state(AddWorker.profession)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.edit_text("Выберите тип работника", reply_markup=markup)


@router.callback_query(F.data == 'delete')
async def workers_type_delete(call: types.CallbackQuery):
    keyboard = [
        [InlineKeyboardButton(text="Мастера", callback_data="delete_master")],
        [InlineKeyboardButton(text="Электромонтеры", callback_data="delete_electrician")],
        [InlineKeyboardButton(text="Испытатели", callback_data="delete_tester")],
        [InlineKeyboardButton(text="АУР (ИТР)", callback_data="delete_aur")],
        [InlineKeyboardButton(text="Назад", callback_data="workers")]
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.edit_text("Выберите тип работника", reply_markup=markup)


@router.callback_query(F.data == 'put')
async def workers_type_update(call: types.CallbackQuery):
    keyboard = [
        [InlineKeyboardButton(text="Мастера", callback_data="put_master")],
        [InlineKeyboardButton(text="Электромонтеры", callback_data="put_electrician")],
        [InlineKeyboardButton(text="Испытатели", callback_data="put_tester")],
        [InlineKeyboardButton(text="АУР (ИТР)", callback_data="put_aur")],
        [InlineKeyboardButton(text="Назад", callback_data="workers")]
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.edit_text("Выберите тип работника", reply_markup=markup)


# @router.callback_query(F.data.startswith('put'))
# async def workers_update(call: types.CallbackQuery):
#     print(call.data.split('_'))


class AddWorker(StatesGroup):
    profession = State()
    name = State()


@router.callback_query(F.data.startswith('add'))
async def workers_update(call: types.CallbackQuery, state: FSMContext):
    message_data = call.data.split('_')
    print(message_data)
    type = WorkType(message_data[1]).name
    await state.update_data(profession=type)
    await call.message.edit_text("Введите Ф.И.О")
    await state.set_state(AddWorker.name)


@router.message(AddWorker.name)
async def add_worker(message: Message, state: FSMContext):
    user_data = await state.get_data()
    worker = Workers(name=message.text, work_type=user_data['profession'])
    db_session.add(worker)
    db_session.commit()
    keyboard = [
        [InlineKeyboardButton(text=f"Вернуться на главную", callback_data="back_main")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await state.clear()
    await message.reply(text="Успешное добавление. Выберите действие",
                        reply_markup=markup)
