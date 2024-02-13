from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db_session
from data.models import Workers, WorkType, Object, Auto

router = Router()


@router.callback_query(F.data == 'auto')
async def workers(call: types.CallbackQuery):
    keyboard = [
        [InlineKeyboardButton(text="Добавить", callback_data="auto_add")],
        [InlineKeyboardButton(text="Удалить", callback_data="auto_delete")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")]
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await call.message.edit_text("Выберите действие", reply_markup=markup)

class AddAuto(StatesGroup):
    name = State()
    isOOO = State()
    isHeavy = State()
    tg = State()

@router.callback_query(F.data == 'auto_add')
async def object_add(call: types.CallbackQuery, state: FSMContext):

    message_data = call.data.split('_')

    print(message_data)

    await call.message.edit_text("Введите имя объекта")
    await state.set_state(AddAuto.name)


@router.message(AddAuto.name)
async def add_name_to_object(message: Message, state: FSMContext):
    print(message.text)

    keyboard = [
        [InlineKeyboardButton(text="OOO", callback_data="auto_form_ooo")],
        [InlineKeyboardButton(text="ИП", callback_data="auto_form_ip")],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.reply("Выберите тип авто", reply_markup=markup)

    await state.update_data(name=message.text)
    await state.set_state(AddAuto.isOOO)
    await message.delete()

@router.callback_query(F.data.startswith("auto_form"))
async def add_form_to_auto(call: types.CallbackQuery, state: FSMContext):


    global isOOO
    keyboard = [
        [InlineKeyboardButton(text="Грузовая", callback_data="auto_weight_heavy")],
        [InlineKeyboardButton(text="Легковая", callback_data="auto_weight_easy")],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.reply("Выберите тип авто", reply_markup=markup)
    if call.data == "auto_form_ooo":
        isOOO = True
    else:
        isOOO = False
    await state.update_data(isOOO=isOOO)

    await state.set_state(AddAuto.isOOO)



@router.callback_query(F.data.startswith("auto_weight"))
async def add_tg_to_object(call: types.CallbackQuery, state: FSMContext):

    global isHeavy
    if call.data == "auto_weight_heavy":
        isHeavy = True
    else:
        isHeavy = False
    await state.update_data(isHeavy=isHeavy)

    await state.set_state(AddAuto.tg)
    await call.message.reply("Введите ссылку на тг")


@router.message(AddAuto.tg)
async def add_tg_to_auto(message: types.Message, state: FSMContext):

    await state.update_data(tg=message.text)
    auto_data = await state.get_data()
    auto = Auto(isOOO=auto_data['isOOO'], isHeavy=auto_data['isHeavy'],
                name=auto_data['name'], tg_link=auto_data['tg'])
    db_session.add(auto)
    db_session.commit()
    keyboard = [
        [InlineKeyboardButton(text=f"Вернуться на главную", callback_data="back_main")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await state.clear()
    await message.reply(text="Успешное добавление. Выберите действие",
                        reply_markup=markup)

@router.callback_query(F.data.startswith('auto_delete'))
async def generate_object_to_delete(call: types.CallbackQuery, state: FSMContext):
    message_data = call.data.split('_')
    print(message_data)

    markup = InlineKeyboardBuilder()
    objects = (db_session.query(Auto)
               .order_by(Auto.name).all())
    print(objects)
    for object in objects:
        markup.button(
            text=f"{object.name}",
            callback_data=f"au_delete_{object.id}"
        )

    markup.button(text="Назад", callback_data="back_main")
    markup.adjust(1)

    await call.message.edit_text("Выберите авто",
                                 reply_markup=markup.as_markup())


@router.callback_query(F.data.startswith('au_delete'))
async def delete_object_to_delete(call: types.CallbackQuery):
    message_data = call.data.split('_')
    id = message_data[2]
    db_session.query(Auto).filter(Auto.id == id).delete()
    db_session.commit()
    keyboard = [
        [InlineKeyboardButton(text=f"Вернуться на главную", callback_data="back_main")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.edit_text("Успешное удаление. Выберите действие",
                                 reply_markup=markup)