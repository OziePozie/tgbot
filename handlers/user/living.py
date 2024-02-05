from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from config import bot
from context.user.main_context import LivingOrders
from keyboard.user.main import performance_report_markup, CallbackWorkersData, CallbackObjectData, date_from, \
    workers_callback_markup, main


router = Router()


@router.callback_query(F.data == "living")
async def living(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выбор Ф.И.О. мастера", reply_markup=workers_callback_markup())
    await state.set_state(LivingOrders.master)


@router.callback_query(LivingOrders.master, CallbackWorkersData.filter())
async def living_master(call: types.CallbackQuery, callback_data: CallbackWorkersData, state: FSMContext):
    await state.update_data(master=callback_data.data)
    await call.message.edit_text("Выбор объекта", reply_markup=performance_report_markup())
    await state.set_state(LivingOrders.object_name)


@router.callback_query(LivingOrders.object_name, CallbackObjectData.filter())
async def living_object(call: types.CallbackQuery, callback_data: CallbackWorkersData, state: FSMContext):
    await state.update_data(object_name=callback_data.data)
    await call.message.answer("Дата с ...", reply_markup=date_from())
    await state.set_state(LivingOrders.worker_date_is)


@router.message(LivingOrders.worker_date_is)
async def living_date(message: types.Message, state: FSMContext):
    await state.update_data(worker_date_is=message.text)
    await message.answer("Дата по ...", reply_markup=date_from())
    await state.set_state(LivingOrders.worker_date_to)


@router.message(LivingOrders.worker_date_to)
async def living_date_to(message: types.Message, state: FSMContext):
    await state.update_data(worker_date_to=message.text)
    await message.answer("Ввод стоимости аренды жилья за период, руб.", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(LivingOrders.price)


@router.message(LivingOrders.price)
async def living_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Ввод номера карты/ номера телефона")
    await state.set_state(LivingOrders.cart_number)


@router.message(LivingOrders.cart_number)
async def living_cart(message: types.Message, state: FSMContext):
    await state.update_data(cart_number=message.text)
    await message.answer("Ф.И.О. получателя")
    await state.set_state(LivingOrders.fio_cart)


@router.message(LivingOrders.fio_cart)
async def living_price(message: types.Message, state: FSMContext):
    await state.update_data(fio_cart=message.text)
    data = await state.get_data()
    await bot.send_message(chat_id=-4104881167, text=f"Прошу перевести {data['price']} за квартиру.\n"
                                                     f"Объект - {data['object_name']}, по номеру {data['cart_number']}\n"
                                                     f"{data['fio_cart']}")
    await message.answer("Выполнено", reply_markup=main())
    await state.clear()