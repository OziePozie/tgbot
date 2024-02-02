from aiogram import Router, F, types
from keyboard.user.main import performance_report_markup

router = Router()


@router.callback_query(F.data == "performance_report")
async def list_work(call: types.CallbackQuery):
    await call.message.edit_text("text", reply_markup=performance_report_markup())


@router.callback_query(F.text == "autocran")
async def autocran(call: types.CallbackQuery):
    pass


@router.callback_query(F.text == "other_expenses")
async def other_expenses(call: types.CallbackQuery):
    pass


@router.callback_query(F.text == "living")
async def living(call: types.CallbackQuery):
    pass


@router.callback_query(F.text == "transport")
async def transport(call: types.CallbackQuery):
    pass


@router.callback_query(F.text == "travel_orders")
async def order_command(call: types.CallbackQuery):
    pass
