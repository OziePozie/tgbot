from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from context.user.main_context import OtherExpenses
from data.models import Object
from keyboard.user.main import workers_callback_markup, CallbackWorkersData, performance_report_markup, \
    CallbackObjectData, main, CallbackWorkersListData, workers_list_callback_markup
from config import bot, db_session

router = Router()


@router.callback_query(F.data == "other_expenses")
async def other_expenses(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выбор Ф.И.О. мастера", reply_markup=workers_list_callback_markup())
    await state.set_state(OtherExpenses.master)


@router.callback_query(CallbackWorkersListData.filter(), OtherExpenses.master)
async def fil_workers_other(call: types.CallbackQuery, callback_data: CallbackWorkersData, state: FSMContext):
    await state.update_data(master=callback_data.data)
    await call.message.edit_text("Выбор объекта", reply_markup=performance_report_markup())
    await state.set_state(OtherExpenses.object_name)


@router.callback_query(CallbackObjectData.filter(), OtherExpenses.object_name)
async def fil_object_other(call: types.CallbackQuery, callback_data: CallbackObjectData, state: FSMContext):
    await state.update_data(object_name=callback_data.action)
    await call.message.answer("Ввод наименование товара", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(OtherExpenses.tovar_name)


@router.message(OtherExpenses.tovar_name)
async def tovar_name_other(message: types.Message, state: FSMContext):
    await state.update_data(tovar_name=message.text)
    await message.answer("Стоимость товара, руб")
    await state.set_state(OtherExpenses.tovar_price)


@router.message(OtherExpenses.tovar_price)
async def tovar_price_other(message: types.Message, state: FSMContext):
    await state.update_data(tovar_price=message.text)
    await message.answer("Добавление фото чека/ УПД")
    await state.set_state(OtherExpenses.photo_check)


@router.message(OtherExpenses.photo_check, F.photo)
async def check_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id
    photo_message = await bot.send_photo(chat_id=-4157476441, photo=photo_id)
    object_name = db_session.query(Object).filter(Object.id == int(data['object_name'])).first()

    await bot.send_message(chat_id=-4157476441, text=f"Мастер: {data['master']}\n"
                                                     f"Обьект: {str(object_name.name)}\n"
                                                     f"Наименование товара: {data['tovar_name']}\n"
                                                     f"Стоимость товара {data['tovar_price']} руб\n",
                           reply_to_message_id=photo_message.message_id)

    object_to_update = db_session.query(Object).filter(Object.id == int(data['object_name'])).first()
    if object_to_update:
        object_to_update.total_other_expenses += float(data['tovar_price'])
        db_session.commit()
        await state.clear()
        await message.answer("Выполнено", reply_markup=main())
    else:
        await message.answer("Попробуйте позже", reply_markup=main())
