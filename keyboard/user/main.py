from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
