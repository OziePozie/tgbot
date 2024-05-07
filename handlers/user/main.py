from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboard.user.main import main
from config import user_password, db_session
from context.user.main_context import UserState
from sqlalchemy import select
from data.models import Auth

router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    user = db_session.scalar(select(Auth).where(Auth.user_id == message.from_user.id))
    if user:
        await message.answer("Добро пожаловать", reply_markup=main())
        await state.clear()
    else:
        await message.answer("Введите пароль")
        await state.set_state(UserState.password)


@router.message(UserState.password)
async def set_password(message: types.Message, state: FSMContext):
    if message.text == user_password:
        new_user = Auth(
            user_id=message.from_user.id)
        db_session.add(new_user)
        db_session.commit()
        await message.answer("Добро пожаловать", reply_markup=main())
        await state.clear()
    else:
        await message.answer("Неверный пароль\n\nПовторите")
