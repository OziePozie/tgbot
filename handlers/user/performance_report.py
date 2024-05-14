from datetime import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from config import db_session, bot
from keyboard.user.main import performance_report_markup, CallbackObjectData, CallbackDateOrdersData, date_of_work, main
from context.user.main_context import PerformanceReport
from data.models import PerformanceReport as PerformanceReportDB, Object, Travel_orders

router = Router()


@router.callback_query(F.data == "performance_report")
async def list_work(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите объект", reply_markup=performance_report_markup())
    await state.set_state(PerformanceReport.object)


@router.callback_query(CallbackObjectData.filter(), PerformanceReport.object)
async def filter_object(call: types.CallbackQuery, callback_data: CallbackObjectData, state: FSMContext):
    await state.update_data(object=callback_data.action)
    check_order = db_session.query(Travel_orders).filter(Travel_orders.from_report == int(call.from_user.id)).all()
    if not check_order :
        await call.message.edit_text("Для начала закажите командировочные", reply_markup=main())
        await state.clear()
    current_date = datetime.now().date().strftime("%d.%m.%Y")
    current_date_obj = datetime.strptime(current_date, "%d.%m.%Y")
    date_to = datetime.strptime(check_order[0].date_to, "%d.%m.%Y")
    if current_date_obj > date_to:
        await call.message.edit_text("Для начала закажите отчет", reply_markup=main())
        await state.clear()
    else:
        await call.message.edit_text("Выберите период", reply_markup=date_of_work(call.from_user.id))
        await state.set_state(PerformanceReport.date)


@router.callback_query(CallbackDateOrdersData.filter(), PerformanceReport.date)
async def date_report(call: types.CallbackQuery, state: FSMContext, callback_data: CallbackDateOrdersData):
    await state.update_data(date=callback_data.data)
    await call.message.edit_text("Напиши отчет о проделанной работе")
    await state.set_state(PerformanceReport.text)


@router.message(PerformanceReport.text)
async def check_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Приложите фото или видео")
    await state.set_state(PerformanceReport.photo_video)


@router.message(PerformanceReport.photo_video, F.photo)
async def check_photo_video(message: types.Message, state: FSMContext):
    await state.update_data(photo_video=message.photo[-1].file_id)
    data = await state.get_data()

    user_id = int(message.from_user.id)

    existing_report = db_session.query(PerformanceReportDB).filter(PerformanceReportDB.user_id == user_id).first()

    if existing_report:
        # Обновляем существующий отчет
        existing_report.object_name = data['object']
        existing_report.date = data['date']
        existing_report.text = data['text']
        existing_report.photo_video = data['photo_video']
        existing_report.is_sendReport = True
    else:
        # Создаем новый отчет
        new_report = PerformanceReportDB(
            object_name=data['object'],
            user_id=user_id,
            date=data['date'],
            text=data['text'],
            photo_video=data['photo_video'],
            is_sendReport=True
        )
        db_session.add(new_report)

    db_session.commit()

    await message.answer("Выполнено!", reply_markup=main())
    object_name = db_session.query(Object).filter(Object.id == int(data['object'])).first()
    chat_id = db_session.query(Object).filter(Object.name == str(object_name.name)).first()
    a = await bot.send_photo(chat_id=int(chat_id.tg_link), photo=data['photo_video'])

    await bot.send_message(chat_id=int(chat_id.tg_link), text=f"Отчет о работе\n"
                                                     f"Объект: {object_name.name}\n"
                                                     f"Период: {data['date']}\n"
                                                     f"Сообщение: {data['text']}\n",
                           reply_to_message_id=a.message_id)

    await state.clear()





