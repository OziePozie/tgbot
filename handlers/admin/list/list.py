from datetime import datetime

from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import db_session, bot
from data.models import Object, PerformanceReport

router = Router()


@router.callback_query(F.data == 'list')
async def report(call: CallbackQuery):
    await call.message.edit_text("Выберите обьект",
                                 reply_markup=generate_object_keyboard())


def generate_object_keyboard():
    markup = InlineKeyboardBuilder()
    objects = (db_session.query(Object)
               .order_by(Object.name).all())
    print(objects)
    for object in objects:
        markup.button(
            text=f"{object.name}",
            callback_data=f"choice_{object.id}"
        )

    markup.button(text="Назад", callback_data="back_main")
    markup.adjust(1)

    return markup.as_markup()


@router.callback_query(F.data.startswith('choice'))
async def choice_object(call: CallbackQuery):
    id = call.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton(text="Отчет по работе", callback_data=f"work_report_{id}")],
        [InlineKeyboardButton(text="Отчет по затратам", callback_data=f"waste_report_{id}")],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.reply("Выберите тип отчета", reply_markup=markup)


@router.callback_query(F.data.startswith('work_report'))
async def work_report(call: CallbackQuery):
    message = call.data.split('_')
    id = message[2]

    keyboard = [
        [InlineKeyboardButton(text="Отчет по работе с фото/видео материалами",
                              callback_data=f"media_report_{id}")],
        [InlineKeyboardButton(text="Журнал КС-6",
                              callback_data=f"ks-6_report_{id}")],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await call.message.reply("Выберите тип отчета", reply_markup=markup)


@router.callback_query(F.data.startswith('waste_report'))
async def waste_report(call: CallbackQuery):
    message = call.data.split('_')
    id = message[2]
    object = db_session.query(Object).filter(Object.id == int(id)).first()

    print(datetime.now())
    print(object.createdAt)

    sum = (object.total_travelers + object.total_autocran
           + object.total_fuel + object.total_living +
           object.total_other_expenses)

    await call.message.reply(f"Отчет по объекту {object.name} \n"
                             f"Количество дней {object.createdAt} \n"
                             f"Командировачные расходы {round(object.total_travelers, 0)} .руб \n"
                             f"Транспортные расходы {round(object.total_fuel, 0)} .руб \n"
                             f"Затраты на проживание {round(object.total_living, 0)} .руб \n"
                             f"Прочие расходы {round(object.total_other_expenses, 0)} .руб \n"
                             f"Затраты на услуги автокрана {round(object.total_autocran, 0)} .руб \n"
                             f"Итого {round(sum, 0)} .руб")


@router.callback_query(F.data.startswith('media_report'))
async def media_report(call: CallbackQuery):
    message = call.data.split('_')
    object = db_session.query(Object).filter(Object.id == int(message[2])).first()
    reports = (db_session.query(PerformanceReport)
              .filter(PerformanceReport.object_name == int(message[2])))

    for report in reports:
        try:
            id = await bot.send_photo(chat_id=call.from_user.id,
                                      photo=report.photo_video)
            await bot.send_message(chat_id=call.from_user.id,
                                   text=f"Отчет по объекту {object.name} \n"
                                        f"Дата: {report.date} \n"
                                        f"{report.text}",
                                   reply_to_message_id=id.message_id)
        except Exception as e:
            pass


@router.callback_query(F.data.startswith('ks-6_report'))
async def ks_6_report(call: CallbackQuery):
    message = call.data.split('_')
    object = db_session.query(Object).filter(Object.id == int(message[2])).first()
    reports = (db_session.query(PerformanceReport)
               .filter(PerformanceReport.object_name == int(message[2])))

    for report in reports:
        await bot.send_message(chat_id=call.from_user.id,
                               text=f"Отчет по объекту {object.name} \n"
                                    f"Дата: {report.date} \n"
                                    f" {report.text}")
