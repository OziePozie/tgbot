from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import db_session
from aiogram.filters.callback_data import CallbackData
from data.models import Object, Workers, Travel_orders, Auto


def main():
    keyboard = [
        [InlineKeyboardButton(text="ОТЧЕТ о работе", callback_data="performance_report")],
        [InlineKeyboardButton(text="АВТОКРАН", callback_data="autocran")],
        [InlineKeyboardButton(text="Прочие расходы", callback_data="other_expenses")],
        [InlineKeyboardButton(text="ПРОЖИВАНИЕ", callback_data="living")],
        [InlineKeyboardButton(text="ТРАНСПОРТ", callback_data="transport")],
        [InlineKeyboardButton(text="ЗАКАЗ командировочных", callback_data="travel_orders")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


class CallbackObjectData(CallbackData, prefix="object_data"):
    action: str
    data: str


def performance_report_markup():
    builder = InlineKeyboardBuilder()
    data = db_session.query(Object.id, Object.name).all()
    for d in data:
        builder.button(
            text=d[1], callback_data=CallbackObjectData(data=d[1], action=str(d[0]))
        )
    builder.adjust(1)
    return builder.as_markup()


class CallbackWorkersData(CallbackData, prefix="workers_data"):
    action: str
    data: str


def workers_callback_markup():
    builder = InlineKeyboardBuilder()
    data = db_session.query(Workers.id, Workers.name).all()

    users = {i[0] for i in db_session.query(Travel_orders.fio).all()}

    for d in data:
        check = [d[1]] if d[1] in users else []
        if not check:
            builder.button(
                text=d[1], callback_data=CallbackWorkersData(data=d[1], action=str(d[0]))
            )
        else:
            pass
    builder.adjust(1)
    return builder.as_markup()


def date_from():
    buttons = []
    now = datetime.now()
    for i in range(20):
        date = now - timedelta(days=i)
        date_str = date.strftime("%d.%m.%Y")
        button = [KeyboardButton(text=date_str)]
        buttons.append(button)

    markup = ReplyKeyboardMarkup(keyboard=buttons)

    return markup


def add_person():
    keyboard = [
        [KeyboardButton(text="Еще добавить")],
        [KeyboardButton(text='Закончить')]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard)
    return markup


class CallbackAutoData(CallbackData, prefix="auto_data"):
    action: str
    data: str


def list_auto_keyboard(callback_data):
    builder = InlineKeyboardBuilder()
    if callback_data == "OOO":
        data = db_session.query(Auto.id, Auto.name).where(Auto.isOOO == 1)
    else:
        data = db_session.query(Auto.id, Auto.name).where(Auto.isOOO == 0)
    for d in data:
        builder.button(
            text=d[1], callback_data=CallbackAutoData(data=d[1], action=str(d[0]))
        )
    builder.adjust(1)
    return builder.as_markup()


def ooo_or_ip():
    buttons = [
        [InlineKeyboardButton(text="ИП", callback_data="IP")],
        [InlineKeyboardButton(text="ООО", callback_data="OOO")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


class CallbackWorkerData(CallbackData, prefix="workers_data"):
    action: str
    data: str


def worker_callback_markup():
    builder = InlineKeyboardBuilder()
    data = db_session.query(Workers.id, Workers.name).all()

    for d in data:
        builder.button(
            text=d[1], callback_data=CallbackWorkersData(data=d[1], action=str(d[0]))
            )

    builder.adjust(1)
    return builder.as_markup()


def go_to_markup():
    buttons = [
        [InlineKeyboardButton(text="Выбор даты выезда с базы на объект", callback_data="vyezd")],
        [InlineKeyboardButton(text="Выбор даты приезда с объекта на базу", callback_data="priezd")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


class CallbackDateFromData(CallbackData, prefix="date_data"):
    action: str
    data: str


def date_from_vyezd(user):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=str(user.date_from), callback_data=CallbackDateFromData(action=str(user.id), data=str(user.date_from))
    )
    builder.adjust(1)
    return builder.as_markup()
