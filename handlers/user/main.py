from aiogram import Router, F, types
from aiogram.filters import Command
from keyboard.user.main import main

router = Router()


@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Добро пожаловать", reply_markup=main())
