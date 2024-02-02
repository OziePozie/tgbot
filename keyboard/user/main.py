from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main():
    keyboard = [
        [KeyboardButton(text="ОТЧЕТ о работе")],
        [KeyboardButton(text="АВТОКРАН")],
        [KeyboardButton(text="Прочие расходы")],
        [KeyboardButton(text="ПРОЖИВАНИЕ")],
        [KeyboardButton(text="ТРАНСПОРТ")],
        [KeyboardButton(text="ЗАКАЗ командировочных")]
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)
    return markup
