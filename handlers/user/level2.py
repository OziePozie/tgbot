from aiogram import Router, F, types

router = Router()


@router.callback_query(F.text == "performance_report")
async def list_work(message: types.Message):
    pass


@router.callback_query(F.text == "autocran")
async def autocran(message: types.Message):
    pass


@router.callback_query(F.text == "other_expenses")
async def other_expenses(message: types.Message):
    pass


@router.callback_query(F.text == "living")
async def living(message: types.Message):
    pass


@router.callback_query(F.text == "transport")
async def transport(message: types.Message):
    pass


@router.callback_query(F.text == "travel_orders")
async def order_command(message: types.Message):
    pass
