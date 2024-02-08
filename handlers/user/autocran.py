from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from config import bot, db_session
from data.models import Object
from context.user.main_context import Autocran
from keyboard.user.main import workers_callback_markup, CallbackWorkersData, performance_report_markup, \
    CallbackObjectData, date_from, main, workers_list_callback_markup, CallbackWorkersListData

router = Router()


@router.callback_query(F.data == "autocran")
async def autocran(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выбор Ф.И.О. мастера", reply_markup=workers_list_callback_markup())
    await state.set_state(Autocran.master)


@router.callback_query(CallbackWorkersListData.filter(), Autocran.master)
async def autocran_workers(call: types.CallbackQuery, callback_data: CallbackWorkersData, state: FSMContext):
    await state.update_data(master=callback_data.data)
    await call.message.edit_text("Выбор объекта", reply_markup=performance_report_markup())
    await state.set_state(Autocran.object_name)


@router.callback_query(CallbackObjectData.filter(), Autocran.object_name)
async def autocran_object(call: types.CallbackQuery, callback_data: CallbackObjectData, state: FSMContext):
    await state.update_data(object_name=callback_data.action)
    await call.message.answer("Выбор даты", reply_markup=date_from())
    await state.set_state(Autocran.date)


@router.message(Autocran.date)
async def autocran_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Ввод стоимости услуг по автокрану, руб.", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Autocran.price)


@router.message(Autocran.price)
async def autocran_date(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Ввод номера карты/ номера телефона.")
    await state.set_state(Autocran.cart_number)


@router.message(Autocran.cart_number)
async def autocran_date(message: types.Message, state: FSMContext):
    await state.update_data(cart_number=message.text)
    await message.answer("Ф.И.О. получателя")
    await state.set_state(Autocran.fio_cart)


@router.message(Autocran.fio_cart)
async def autocran_date(message: types.Message, state: FSMContext):
    await state.update_data(fio_cart=message.text)
    data = await state.get_data()
    object_to_update = db_session.query(Object).filter(Object.id == int(data['object_name'])).first()
    if object_to_update:
        object_to_update.total_autocran += float(data['price'])
        db_session.commit()
        await bot.send_message(chat_id=-4104881167, text=f"Прошу перевести {data['price']} руб за автокран \n"
                                                         f"Обьект: {data['object_name']} \n"
                                                         f"по номеру {data['cart_number']}\n"
                                                         f"Ф.И.О. получателя: {data['fio_cart']}")
        await state.clear()
        await message.answer("Выполнено", reply_markup=main())
    else:
        await message.answer("Попробуйте позже", reply_markup=main())

