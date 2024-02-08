from datetime import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from context.user.main_context import TravelOrdersReport
from keyboard.user.main import performance_report_markup, CallbackObjectData, \
    CallbackWorkersData, workers_callback_markup, date_from, add_person, main
from data.models import Travel_orders
from config import db_session, bot

router = Router()


@router.callback_query(F.data == "travel_orders")
async def order_command(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выбор объекта", reply_markup=performance_report_markup())
    await state.set_state(TravelOrdersReport.object_name)


@router.callback_query(CallbackObjectData.filter(), TravelOrdersReport.object_name)
async def fil_object(call: types.CallbackQuery, callback_data: CallbackObjectData, state: FSMContext):
    await state.update_data(object_name=callback_data.data)
    await call.message.edit_text("Выбор Ф.И.О. членов бригады", reply_markup=workers_callback_markup())
    await state.set_state(TravelOrdersReport.worker_name)


@router.callback_query(CallbackWorkersData.filter(), TravelOrdersReport.worker_name)
async def fil_workers(call: types.CallbackQuery, callback_data: CallbackWorkersData, state: FSMContext):
    await state.update_data(worker_name=callback_data.data)
    await call.message.answer("Дата с ...", reply_markup=date_from())
    await state.set_state(TravelOrdersReport.worker_date_is)


@router.message(TravelOrdersReport.worker_date_is)
async def fil_date(message: types.Message, state: FSMContext):
    await state.update_data(worker_date_is=message.text)
    await message.answer("Дата по ...", reply_markup=date_from())
    await state.set_state(TravelOrdersReport.worker_date_to)


@router.message(TravelOrdersReport.worker_date_to)
async def fil_date_to(message: types.Message, state: FSMContext):
    await state.update_data(worker_date_to=message.text)
    data = await state.get_data()
    try:
        new_worker = Travel_orders(fio=data['worker_name'],
                                   date_from=data['worker_date_is'],
                                   date_to=data['worker_date_to'],
                                   from_report=message.from_user.id,
                                   is_order=True,
                                   object_name=data['object_name'])
        db_session.add(new_worker)
        db_session.commit()
        await message.answer(f"Пользователь {data['worker_name']} добавлен в отчет", reply_markup=add_person())
        await state.clear()
    except ValueError as e:
        await message.answer("Попробуйте заново!")
        await state.clear()


@router.message(F.text == "Еще добавить")
async def add_person_any(message: types.Message, state: FSMContext):
    await message.answer("Выбор Ф.И.О. членов бригады", reply_markup=performance_report_markup())
    await state.set_state(TravelOrdersReport.object_name)


@router.message(F.text == 'Закончить')
async def quit(message: types.Message):
    text = "Объект: \n"
    from_report = str(message.from_user.username)
    users = db_session.query\
        (Travel_orders.fio, Travel_orders.date_from, Travel_orders.date_to, Travel_orders.object_name).filter\
        (Travel_orders.from_report == from_report)
    for user in users:
        delta = (datetime.strptime(user.date_to, '%d.%m.%Y') - datetime.strptime(user.date_from, '%d.%m.%Y')).days
        text += f"{user[0]} – {delta} дней; \n"
    text = text[:-2] + "\n"
    await bot.send_message(chat_id=-4104881167, text=text)
    await message.answer("Выполнено!", reply_markup=main())


