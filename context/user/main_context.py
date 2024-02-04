from aiogram.fsm.state import StatesGroup, State


class TravelOrdersReport(StatesGroup):
    object_name = State()
    worker_name = State()
    worker_date_is = State()
    worker_date_to = State()

