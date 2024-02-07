from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from config import db_session
from service.geopy_service import get_km
from context.user.main_context import Transport
from keyboard.user.main import CallbackWorkerData, CallbackObjectData, \
    performance_report_markup, list_auto_keyboard, CallbackAutoData, ooo_or_ip, worker_callback_markup, go_to_markup, \
    date_from, main
from data.models import Transports

router = Router()


@router.callback_query(F.data == "transport")
async def transport(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выбор Ф.И.О. мастера", reply_markup=worker_callback_markup())
    await state.set_state(Transport.master)


@router.callback_query(CallbackWorkerData.filter(), Transport.master)
async def transport_master(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackWorkerData):
    await state.update_data(master=callback_data.data)
    await call.message.edit_text("Выбор объекта", reply_markup=performance_report_markup())
    await state.set_state(Transport.object_name)


@router.callback_query(CallbackObjectData.filter(), Transport.object_name)
async def transport_object(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackAutoData):
    await state.update_data(object_name=callback_data.data)
    await call.message.edit_text("ООО или ИП?", reply_markup=ooo_or_ip())
    await state.set_state(Transport.ooo_or_ip)


@router.callback_query(Transport.ooo_or_ip, F.data == "IP")
async def transport_IP(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(ooo_or_ip=call.data)
    await call.message.edit_text("Выбор авто", reply_markup=list_auto_keyboard(callback_data=call.data))
    await state.set_state(Transport.auto)


@router.callback_query(Transport.ooo_or_ip, F.data == "OOO")
async def transport_OOO(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(ooo_or_ip=call.data)
    await call.message.edit_text("Выбор авто", reply_markup=list_auto_keyboard(callback_data=call.data))
    await state.set_state(Transport.auto)


@router.callback_query(CallbackAutoData.filter(), Transport.auto)
async def transport_auto(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackAutoData):
    await state.update_data(auto=callback_data.data)
    data = await state.get_data()
    if data['ooo_or_ip'] == "OOO":
        await call.message.edit_text("Выбор", reply_markup=go_to_markup())
    else:
        await call.message.edit_text("Напишите город прибытия?")
        await state.set_state(Transport.city)


@router.callback_query(F.data == "vyezd")
async def transport_vyezd(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Выбор даты", reply_markup=date_from())
    await state.set_state(Transport.date_from)


@router.message(Transport.date_from)
async def transport_date(message: types.Message, state: FSMContext):
    await state.update_data(date_from=message.text)
    data = await state.get_data()
    try:
        if data['ooo_or_ip'] == 'IP':
            transport = Transports(
                master=data['master'],
                master_id=message.from_user.id,
                object_name=data['object_name'],
                ooo_or_ip=data['ooo_or_ip'],
                auto=data['auto'],
                city=data['city'],
                km=data['km'],
                date_from=data['date_from']
            )
            db_session.add(transport)
            db_session.commit()
            await message.answer("Принято!", reply_markup=main())
            await state.clear()

        else:
            transport = Transports(
                master=data['master'],
                master_id=message.from_user.id,
                object_name=data['object_name'],
                ooo_or_ip=data['ooo_or_ip'],
                auto=data['auto'],
                date_from=data['date_from']
            )
            db_session.add(transport)
            db_session.commit()
            await message.answer("Принято!", reply_markup=main())
            await state.clear()
    except Exception as ex:
        await message.answer(f"Ошибка при добавлении! Попробуйте снова {ex}")


@router.callback_query(F.data == "priezd")
async def transport_priezd(call: types.CallbackQuery):
    pass


@router.message(Transport.city)
async def transport_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    km = get_km(str(message.text))
    await state.update_data(km=km)
    await message.answer("Выбор", reply_markup=go_to_markup())



