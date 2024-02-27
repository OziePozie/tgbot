from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from keyboard.user.main import transport_master_list, CallbackTransportList, main
from context.user.main_context import UpdateKM
from data.models import Transports
from config import db_session

router = Router()


@router.callback_query(F.data == "update_probeg")
async def add_probeg(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите мастера", reply_markup=transport_master_list())
    await state.set_state(UpdateKM.user)


@router.callback_query(CallbackTransportList.filter(), UpdateKM.user)
async def set_name(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackTransportList):
    await state.update_data(user=callback_data.data)
    await call.message.edit_text("Введите данный пробег")
    await state.set_state(UpdateKM.km)


@router.message(UpdateKM.km)
async def update_km(message: types.Message, state: FSMContext):
    await state.update_data(km=message.text)
    data = await state.get_data()
    try:
        master_name = db_session.query(Transports).filter(Transports.master == str(data['user'])).first()
        master_name.probeg_prized = int(data['km'])
        db_session.commit()
        await message.answer("Принято", reply_markup=main())
        await state.clear()
    except Exception as e:
        await message.answer(f"{e}", reply_markup=main())
        await state.clear()