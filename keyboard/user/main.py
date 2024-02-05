from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import db_session
from aiogram.filters.callback_data import CallbackData
from data.models import Object, Workers, Travel_orders


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
