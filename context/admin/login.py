from aiogram.fsm.state import StatesGroup, State


class AdminLogin(StatesGroup):
    login = State()
    password = State()
