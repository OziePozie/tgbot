from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import db_session
from sqlalchemy.future import select
from aiogram.filters.callback_data import CallbackData
from data.models import Object, Workers, Travel_orders, Auto, PerformanceReport, Transports


def main():
    keyboard = [
        [InlineKeyboardButton(text="ОТЧЕТ о работе", callback_data="performance_report")],
        [InlineKeyboardButton(text="Добавить промежуточный пробег", callback_data="update_probeg")],
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
    builder.button(text="В главное меню", callback_data="back_menu")
    builder.adjust(1)
    return builder.as_markup()


class CallbackWorkersData(CallbackData, prefix="workers_data"):
    action: str
    data: str


def workers_callback_markup(message_id):
    builder = InlineKeyboardBuilder()
    data = db_session.query(Workers.id, Workers.name).all()

    current_date = datetime.today().strftime('%d.%m.%Y')
    date_from = db_session.scalars(select(Travel_orders).where(Travel_orders.from_report == message_id))

    if not date_from:
        pass
    else:
        for date in date_from:
            if current_date == date.date_to:
                db_session.delete(date)
                db_session.commit()
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
    for i in range(26):
        date = now + timedelta(days=i)
        date_str = date.strftime("%d.%m.%Y")
        button = [KeyboardButton(text=date_str)]
        buttons.append(button)

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return markup


def add_person():
    keyboard = [
        [KeyboardButton(text="Еще добавить")],
        [KeyboardButton(text='Закончить')]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return markup


class CallbackAutoData(CallbackData, prefix="auto_data"):
    action: str
    data: str


def list_auto_keyboard():
    builder = InlineKeyboardBuilder()
    data = db_session.query(Auto.id, Auto.name).all()
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


class CallbackDateOrdersData(CallbackData, prefix="orders_data"):
    action: str
    data: str


def date_of_work(user_id):
    builder = InlineKeyboardBuilder()
    date_from_db = db_session.query(Travel_orders).filter(Travel_orders.from_report == int(user_id)).first()
    # check_send_order = db_session.query(PerformanceReport).filter(PerformanceReport.user_id == user_id).first()
    current_date = datetime.now().date().strftime("%d.%m.%Y")

    if date_from_db:
        date_from = datetime.strptime(date_from_db.date_from, "%d.%m.%Y")
        date_to = datetime.strptime(date_from_db.date_to, "%d.%m.%Y")

        if date_from < date_to:
            builder.button(
                text=f"{current_date}",
                callback_data=CallbackDateOrdersData(action=f"{str(date_from_db.date_from)}",
                                                     data=f"{str(date_from_db.date_from)}")
            )
    builder.adjust(1)
    return builder.as_markup()


class CallbackWorkersListData(CallbackData, prefix="workerslist_data"):
    action: str
    data: str


def workers_list_callback_markup():
    builder = InlineKeyboardBuilder()
    data = db_session.query(Workers.id, Workers.name).all()

    for d in data:
        builder.button(
            text=d[1], callback_data=CallbackWorkersListData(data=d[1], action=str(d[0]))
        )

    builder.button(text="В главное меню", callback_data="back_menu")
    builder.adjust(1)
    return builder.as_markup()


class CallbackTransportList(CallbackData, prefix="transport"):
    data: str
    action: str


def transport_master_list():
    builder = InlineKeyboardBuilder()
    data = db_session.query(Transports.id, Transports.master).all()

    for d in data:
        builder.button(
            text=d[1], callback_data=CallbackTransportList(data=d[1], action=str(d[0]))
        )
    builder.button(text="В главное меню", callback_data="back_menu")
    builder.adjust(1)
    return builder.as_markup()

