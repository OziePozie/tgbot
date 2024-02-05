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


