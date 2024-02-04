from aiogram import Router, F, types


router = Router()


@router.callback_query(F.text == "other_expenses")
async def other_expenses(call: types.CallbackQuery):
    pass