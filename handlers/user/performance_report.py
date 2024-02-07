from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from keyboard.user.main import performance_report_markup, CallbackObjectData

router = Router()

#
# @router.callback_query(F.data == "performance_report")
# async def list_work(call: types.CallbackQuery, state: FSMContext):
#     await call.message.edit_text("Выберите объект", reply_markup=performance_report_markup())
#
#
# @router.callback_query(CallbackObjectData.filter())
# async def filter_object(call: types.CallbackQuery, callback_data: CallbackObjectData, state: FSMContext):
#     await state.update_data(id=callback_data)
#     await call.message.edit_text("Выберите период")
#
#
# @router.callback_query()
# async def date_report(call: types.CallbackQuery, state: FSMContext):
#     await call.message.edit_text("")


