from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import db_session
from aiogram.filters.callback_data import CallbackData
from data.models import Object


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


def performance_report_markup():
    builder = InlineKeyboardBuilder()
    data = db_session.query(Object.id, Object.name).all()
    for d in data:
        builder.button(
            text=d[1], callback_data=CallbackObjectData(action=str(d[0]))
        )
    builder.adjust(1)
    print(builder.as_markup())
    return builder.as_markup()

