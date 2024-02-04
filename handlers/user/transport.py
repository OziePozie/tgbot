from aiogram import Router, F, types


router = Router()


@router.callback_query(F.text == "transport")
async def transport(call: types.CallbackQuery):
    pass
