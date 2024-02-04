from aiogram import Router, F, types


router = Router()


@router.callback_query(F.text == "autocran")
async def autocran(call: types.CallbackQuery):
    pass