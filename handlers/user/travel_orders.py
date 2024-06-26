from datetime import datetime
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from context.user.main_context import TravelOrdersReport
from keyboard.user.main import performance_report_markup, CallbackObjectData, \
    CallbackWorkersData, workers_callback_markup, date_from, add_person, main
from data.models import Travel_orders, Object
from sqlalchemy import select
from config import db_session, bot

router = Router()


@router.callback_query(F.data == "travel_orders")
async def order_command(call: types.CallbackQuery, state: FSMContext):
    today = datetime.today()
    order = db_session.scalar(select(Travel_orders).where(Travel_orders.from_report == call.from_user.id))
    if not order:
        await call.message.edit_text("Выбор объекта", reply_markup=performance_report_markup())
        await state.set_state(TravelOrdersReport.object_name)
    else:
        date_to = datetime.strptime(order.date_to, '%d.%m.%Y')
        if today >= date_to:
            order_from = db_session.scalar(select(Travel_orders).where(Travel_orders.from_report == call.from_user.id))
            await call.message.edit_text("Это вы?", reply_markup=)
        else:
            print('a')


@router.callback_query(CallbackObjectData.filter(), TravelOrdersReport.object_name)
async def fil_object(call: types.CallbackQuery, callback_data: CallbackObjectData, state: FSMContext):
    await state.update_data(object_name=callback_data.action)

    await call.message.edit_text("Выбор Ф.И.О. членов бригады", reply_markup=workers_callback_markup(call.from_user.id))
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
    user_id = int(message.from_user.id)
    check_data = db_session.query(Travel_orders).filter(Travel_orders.from_report == user_id).first()
    data = await state.get_data()
    try:
        if not check_data:
            new_worker = Travel_orders(fio=data['worker_name'],
                                       date_from=data['worker_date_is'],
                                       date_to=data['worker_date_to'],
                                       from_report=message.from_user.id,
                                       is_order=False,
                                       object_name=data['object_name'])
            db_session.add(new_worker)
            db_session.commit()
            await state.clear()
            await message.answer(f"Пользователь {data['worker_name']} добавлен в отчет", reply_markup=add_person())
        else:
            new_worker = Travel_orders(fio=data['worker_name'],
                                       date_from=data['worker_date_is'],
                                       date_to=data['worker_date_to'],
                                       from_report=message.from_user.id,
                                       is_order=False,
                                       object_name=str(check_data.object_name))
            db_session.add(new_worker)
            db_session.commit()
            await state.clear()
            await message.answer(f"Пользователь {data['worker_name']} добавлен в отчет", reply_markup=add_person())
    except ValueError as e:
        await message.answer("Попробуйте заново!")
        await state.clear()


@router.message(F.text == "Еще добавить")
async def add_person_any(message: types.Message, state: FSMContext):
    await message.answer("Выбор Ф.И.О. членов бригады", reply_markup=workers_callback_markup(message.from_user.id))
    await state.set_state(TravelOrdersReport.worker_name)


@router.message(F.text == 'Закончить')
async def quit(message: types.Message):
    from_report = str(message.from_user.id)
    total_days = 0
    object_id = db_session.query(Travel_orders.object_name).filter(Travel_orders.from_report == from_report).first()
    object_name = db_session.query(Object).filter(Object.id == object_id.object_name).first()
    users = db_session.query \
        (Travel_orders.fio, Travel_orders.date_from, Travel_orders.date_to, Travel_orders.object_name,
         Travel_orders.is_order).filter \
        (Travel_orders.from_report == from_report)
    dates = db_session.query(Travel_orders).filter(Travel_orders.from_report == from_report).first()
    text = (f"С {str(dates.date_from)} по"
            f" {str(dates.date_to)} \n"
            f"Объект: {str(object_name.name)}\n" \
            f"Прошу перевести командировочные:\n")

    for user in users:
        if user[4] is False:
            delta = (datetime.strptime(user.date_to, '%d.%m.%Y') - datetime.strptime(user.date_from, '%d.%m.%Y')).days
            text += f"{user[0]} – {delta} дней - {delta * 700} руб; \n"
            total_days += delta
            # user.is_order = True
    text = text[:-2] + "\n"
    object_to_update = db_session.query(Object).filter(Object.id == int(object_id[0])).first()
    if object_to_update:
        total_sum = total_days * 700
        object_to_update.total_travelers += float(total_sum)
        db_session.commit()
        check_send_order = db_session.query(Travel_orders).filter(Travel_orders.from_report == from_report).all()
        if check_send_order:
            for i in check_send_order:
                i.is_order = True
                db_session.commit()
        await message.answer("Выполнено", reply_markup=main())
        # await bot.send_message(chat_id=-4104881167, text=text)
        await bot.send_message(chat_id=-4156766513, text=text)

        # db_session.query(Travel_orders).filter(Travel_orders.from_report == from_report).delete()
        # db_session.commit()

    else:
        await message.answer("Попробуйте позже", reply_markup=main())
