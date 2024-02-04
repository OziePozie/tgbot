from aiogram import Router, F, types


router = Router()


@router.callback_query(F.text == "living")
async def living(call: types.CallbackQuery):
    pass