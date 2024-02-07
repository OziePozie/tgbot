from aiogram.fsm.state import StatesGroup, State


class TravelOrdersReport(StatesGroup):
    object_name = State()
    worker_name = State()
    worker_date_is = State()
    worker_date_to = State()


class LivingOrders(StatesGroup):
    master = State()
    object_name = State()
    worker_date_is = State()
    worker_date_to = State()
    price = State()
    cart_number = State()
    fio_cart = State()


class OtherExpenses(StatesGroup):
    master = State()
    object_name = State()
    tovar_name = State()
    tovar_price = State()
    photo_check = State()


class Autocran(StatesGroup):
    master = State()
    object_name = State()
    date = State()
    price = State()
    cart_number = State()
    fio_cart = State()


class Transport(StatesGroup):
    master = State()
    object_name = State()
    auto = State()
    ooo_or_ip = State()
    city = State()
    km = State()
    date_from = State()
    probeg = State()

