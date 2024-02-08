from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from config import db_session, bot
from keyboard.user.main import performance_report_markup, CallbackObjectData, CallbackDateOrdersData, date_of_work, main
from context.user.main_context import PerformanceReport
from data.models import PerformanceReport as PerformanceReportDB, Object

router = Router()


@router.callback_query(F.data == "performance_report")
async def list_work(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Выберите объект", reply_markup=performance_report_markup())
    await state.set_state(PerformanceReport.object)


@router.callback_query(CallbackObjectData.filter(), PerformanceReport.object)
async def filter_object(call: types.CallbackQuery, callback_data: CallbackObjectData, state: FSMContext):
    await state.update_data(object=callback_data.action)
    await call.message.edit_text("Выберите период", reply_markup=date_of_work())
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


@router.message(PerformanceReport.photo_video,  F.photo)
async def check_photo_video(message: types.Message, state: FSMContext):
    await state.update_data(photo_video=message.photo[-1].file_id)
    data = await state.get_data()
    new = PerformanceReportDB(
        object_name=data['object'],
        date=data['date'],
        text=data['text'],
        photo_video=data['photo_video']
    )
    db_session.add(new)
    db_session.commit()
    await message.answer("Выполнено!", reply_markup=main())
    a = await bot.send_photo(chat_id=-4104881167, photo=f"{data['photo_video']}")
    object_name = db_session.query(Object).filter(Object.id == int(data['object'])).first()

    await bot.send_message(chat_id=-4104881167, text=f"Отчет о работе\n"
                                                     f"Обьект: {str(object_name.name)}\n"
                                                     f"Период: {data['date']}\n"
                                                     f"Сообщение: {data['text']}\n", reply_to_message_id=a.message_id)
    await state.clear()




