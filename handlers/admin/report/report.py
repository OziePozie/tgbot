import types

from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from .worker.put import router as put_router
from .worker.add import router as add_router
from .worker.delete import router as delete_router
from .object.object import router as object_router

report_router = Router()
report_router.include_router(put_router)
report_router.include_router(add_router)
report_router.include_router(delete_router)
report_router.include_router(object_router)


@report_router.callback_query(F.data == 'report')
async def report(call: CallbackQuery):
    keyboard = [
        [InlineKeyboardButton(text="Персонал", callback_data="workers")],
        [InlineKeyboardButton(text="Объект", callback_data="object")],
        [InlineKeyboardButton(text="Авто", callback_data="auto")],
        [InlineKeyboardButton(text="Назад", callback_data="back_main")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await call.message.edit_text("Выберите действие", reply_markup=markup)