from datetime import datetime, timedelta
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from config import db_session, bot
from service.geopy_service import get_km
from context.user.main_context import Transport
from keyboard.user.main import CallbackWorkerData, CallbackObjectData, \
    performance_report_markup, list_auto_keyboard, CallbackAutoData, ooo_or_ip, worker_callback_markup, go_to_markup, \
    date_from, main, date_from_vyezd, CallbackDateFromData, CallbackWorkersListData, workers_list_callback_markup
from data.models import Transports, Auto, Object
from sqlalchemy import and_

router = Router()


@router.callback_query(F.data == "transport")
async def transport(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выбор Ф.И.О. мастера", reply_markup=workers_list_callback_markup())
    await state.set_state(Transport.master)


@router.callback_query(CallbackWorkersListData.filter(), Transport.master)
async def transport_master(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackWorkerData):
    await state.update_data(master=callback_data.data)
    await call.message.edit_text("Выбор объекта", reply_markup=performance_report_markup())
    await state.set_state(Transport.object_name)


@router.callback_query(CallbackObjectData.filter(), Transport.object_name)
async def transport_object(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackAutoData):
    await state.update_data(object_name=callback_data.data)
    await call.message.edit_text("Выбор авто", reply_markup=list_auto_keyboard())
    await state.set_state(Transport.auto)


@router.callback_query(CallbackAutoData.filter(), Transport.auto)
async def transport_auto(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackAutoData):
    await state.update_data(auto=callback_data.data)

    await call.message.edit_text("Напишите город прибытия?")
    await state.set_state(Transport.city)


@router.callback_query(F.data == "vyezd")
async def transport_vyezd(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = db_session.query(Transports).filter(
        and_(
            Transports.master == str(data['master']),
            Transports.master_id == str(call.from_user.id),
            Transports.priezd == False)).first()
    if user:
        await call.message.answer("Выбор даты", reply_markup=date_from_vyezd(user))
        await state.set_state(Transport.date_from)
    else:
        await call.message.answer("Выбор даты", reply_markup=date_from())
        await state.set_state(Transport.date_from)


@router.callback_query(CallbackDateFromData.filter(), Transport.date_from)
async def check_date(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackDateFromData):
    await state.update_data(date_from=callback_data.data)
    await call.message.edit_text("Введите пробег")
    await state.set_state(Transport.probeg)


@router.message(Transport.date_from)
async def transport_date(message: types.Message, state: FSMContext):
    await state.update_data(date_from=message.text)
    await message.answer("Введите пробега", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Transport.probeg)


@router.message(Transport.probeg)
async def check_probeg(message: types.Message, state: FSMContext):
    await state.update_data(probeg=message.text)
    data = await state.get_data()
    try:
        check_priezd = db_session.query(Transports).filter(Transports.master_id == message.from_user.id).first()
        if check_priezd is None:
            date_obj = datetime.strptime(data['date_from'], "%d.%m.%Y")
            next_message = date_obj + timedelta(days=15)
            next_message_formatted = next_message.strftime("%d.%m.%Y")
            transport = Transports(
                master=data['master'],
                master_id=message.from_user.id,
                object_name=data['object_name'],
                auto=data['auto'],
                city=data['city'],
                km=data['km'],
                date_from=data['date_from'],
                probeg_vyezd=int(data['probeg']),
                next_message=next_message_formatted
            )
            db_session.add(transport)
            db_session.commit()
            await message.answer("Принято!", reply_markup=main())
            chat_id = db_session.query(Auto).filter(Auto.name == str(data['auto'])).first()
            if chat_id.isOOO is False:
                await bot.send_message(chat_id=-4113562102, text=f"Дата выезда {data['date_from']}; \n"
                                                                 f"Маршрут г. Энгельс Саратовская обл. – н.п. {data['city']};\n"
                                                                 f"Расстояние {int(data['km'])} км;\n"
                                                                 f"Стоимость перевозки, руб: {int(data['km']) * 40}")
            # await bot.send_message(chat_id=int(chat_id.tg_link), text=f"Дата выезда {data['date_from']}; \n"
            #                                                  f"Маршрут г. Энгельс Саратовская обл. – н.п. {data['city']};\n"
            #                                                  f"Расстояние {int(data['km'])} км;\n"
            #                                                 )
            # await bot.send_message(chat_id=int(chat_id.tg_link),
            #                        text=f"Выезд с базы"
            #                             f"«Дата: {data['date_from']} - Пробег: {data['probeg']} км»\n"
            #                             f"Мастер: {data['master']}\n"
            #                             f"Объект: {data['object_name']}")
                await state.clear()
        elif check_priezd.priezd is False and check_priezd.probeg_vyezd:
            chat_id = db_session.query(Auto).filter(Auto.name == str(data['auto'])).first()
            await bot.send_message(chat_id=int(chat_id.tg_link),
                                   text=f"Выезд с базы"
                                        f"«Дата: {data['date_from']} - Пробег: {data['probeg']} км»\n"
                                        f"Мастер: {data['master']}\n"
                                        f"Объект: {data['object_name']}")
            await state.clear()
        elif check_priezd.priezd is True:
            user = db_session.query(Transports).filter(Transports.master_id == str(message.from_user.id)).first()
            user.probeg_prized = int(message.text)
            db_session.commit()
            auto_name = db_session.query(Transports.auto).filter(
                Transports.master_id == int(message.from_user.id)).first()
            get_heavy = db_session.query(Auto.isHeavy, Auto.isOOO).filter(Auto.name == str(auto_name.auto)).first()
            current_date = datetime.now().date()
            user = db_session.query(Transports).filter(Transports.master_id == str(message.from_user.id)).first()
            if get_heavy[0] is True:
                probeg = db_session.query(Transports.probeg_vyezd, Transports.probeg_prized,
                                          Transports.object_name).filter(
                    Transports.master_id == int(message.from_user.id)).first()
                raznica = int(probeg.probeg_prized) - int(probeg.probeg_vyezd)
                obshaya_raznica = (int(raznica) * (20 / 100)) * 60
                object_to_update = db_session.query(Object).filter(Object.name == str(probeg.object_name)).first()
                if object_to_update:
                    object_to_update.total_fuel += float(obshaya_raznica)
                    db_session.commit()
                    chat_id = db_session.query(Auto).filter(Auto.name == str(data['auto'])).first()
                    if get_heavy[1] is False:
                        await bot.send_message(chat_id=-4113562102, text=f"Дата приезда {current_date}; \n"
                                                                         f"Маршрут г. Энгельс Саратовская обл. – н.п. {user.city};\n"
                                                                         f"Расстояние {int(user.km)} км;\n"
                                                                         f"Стоимость перевозки, руб: {int(user.km) * 40}")
                        await bot.send_message(chat_id=int(chat_id.tg_link), text=f"Дата приезда {current_date}; \n"
                                                                         f"Маршрут г. Энгельс Саратовская обл. – н.п. {user.city};\n"
                                                                         f"Расстояние {int(user.km)} км;\n"
                                                                         )
                        await state.clear()
                        db_session.query(Transports).filter(Transports.master_id == int(message.from_user.id)).delete()
                        db_session.commit()
                        await message.answer("Принято!", reply_markup=main())
                    else:
                        await bot.send_message(chat_id=-4113562102, text=f"Дата приезда {current_date}; \n"
                                                                         f"Маршрут г. Энгельс Саратовская обл. – н.п. {user.city};\n"
                                                                         f"Расстояние {int(user.km)} км;\n"
                                                                         f"Стоимость перевозки, руб: {int(user.km) * 40}")
                        await state.clear()
                        db_session.query(Transports).filter(Transports.master_id == int(message.from_user.id)).delete()
                        db_session.commit()
                        await message.answer("Принято!", reply_markup=main())
            else:
                probeg = db_session.query(Transports.probeg_vyezd, Transports.probeg_prized,
                                          Transports.object_name).filter(
                    Transports.master_id == int(message.from_user.id)).first()
                raznica = int(probeg.probeg_prized) - int(probeg.probeg_vyezd)
                obshaya_raznica = (int(raznica) * (9 / 100)) * 55
                object_to_update = db_session.query(Object).filter(Object.name == str(probeg.object_name)).first()
                if object_to_update:
                    object_to_update.total_fuel += float(obshaya_raznica)
                    db_session.commit()
                    chat_id = db_session.query(Auto).filter(Auto.name == str(data['auto'])).first()
                    if get_heavy[1] is False:
                        await bot.send_message(chat_id=-4113562102, text=f"Дата приезда {current_date}; \n"
                                                                         f"Маршрут г. Энгельс Саратовская обл. – н.п. {user.city};\n"
                                                                         f"Расстояние {int(user.km)} км;\n"
                                                                         f"Стоимость перевозки, руб: {int(user.km) * 40}")
                        await bot.send_message(chat_id=int(chat_id.tg_link), text=f"Дата приезда {current_date}; \n"
                                                                                  f"Маршрут г. Энгельс Саратовская обл. – н.п. {user.city};\n"
                                                                                  f"Расстояние {int(user.km)} км;\n"
                                                                                 )
                        db_session.query(Transports).filter(Transports.master_id == int(message.from_user.id)).delete()
                        db_session.commit()
                        await state.clear()
                        await message.answer("Принято!", reply_markup=main())
                    else:
                        await bot.send_message(chat_id=-4113562102, text=f"Дата приезда {current_date}; \n"
                                                                         f"Маршрут г. Энгельс Саратовская обл. – н.п. {user.city};\n"
                                                                         f"Расстояние {int(user.km)} км;\n"
                                                                         f"Стоимость перевозки, руб: {int(user.km) * 40}")
                        await state.clear()
                        db_session.query(Transports).filter(Transports.master_id == int(message.from_user.id)).delete()
                        db_session.commit()
                        await message.answer("Принято!", reply_markup=main())
    except Exception as ex:
        await message.answer(f"Ошибка при добавлении! Попробуйте снова {ex}", reply_markup=main())
        await state.clear()


@router.callback_query(F.data == "priezd")
async def transport_priezd(call: types.CallbackQuery, state: FSMContext):
    user = db_session.query(Transports).filter(Transports.master_id == str(call.from_user.id)).first()
    user.priezd = True
    db_session.commit()
    await call.message.answer("Введите пробега")
    await state.set_state(Transport.probeg)


@router.message(Transport.city)
async def transport_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    km = get_km(str(message.text))
    if km is False:
        await state.update_data(km=0)
        await message.answer("Обратитесь к администратору. Не удалось рассчитать расстояние",
                             reply_markup=go_to_markup())
    else:
        await state.update_data(km=km)
        await message.answer("Выбор", reply_markup=go_to_markup())
