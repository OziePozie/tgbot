from aiogram import Router, F, types

router = Router()


@router.message(F.text == "ОТЧЕТ о работе")
async def list_work(message: types.Message):
    pass


@router.message(F.text == "АВТОКРАН")
async def autocran(message: types.Message):
    pass


@router.message(F.text == "Прочие расходы")
async def other_expenses(message: types.Message):
    pass


@router.message(F.text == "ПРОЖИВАНИЕ")
async def living(message: types.Message):
    pass


@router.message(F.text == "ТРАНСПОРТ")
async def transport(message: types.Message):
    pass


@router.message(F.text == "ЗАКАЗ командировочных")
async def order_command(message: types.Message):
    pass
