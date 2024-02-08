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

    await call.message.reply(f"Отчет по объекту {object.name}"
                             f"Количество дней {object.createdAt}"
                             f"Командировачные расходы {object.total_travelers} .руб"
                             f"Транспортные расходы {object.total_fuel} .руб"
                             f"Затраты на проживание {object.total_living} .руб"
                             f"Прочие расходы {object.total_other_expenses} .руб"
                             f"Затраты на услуги автокрана {object.total_autocran} .руб"
                             f"Итого {sum} .руб")


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
        except Exception as e:
            pass
        await bot.send_message(chat_id=call.from_user.id,
                               text=f"Отчет по объекту {object.name} \n"
                                f"Дата: {report.date} \n"
                                f" {report.text}",
                               reply_to_message_id=id.message_id)




@router.callback_query(F.data.startswith('ks_6_report'))
async def ks_6_report(call: CallbackQuery):
    message = call.data.split('_')
    object = db_session.query(Object).filter(Object.id == int(message[2])).first()
    reports = (db_session.query(PerformanceReport)
               .filter(PerformanceReport.object_name == int(message[2])))

    for report in reports:
        await bot.send_message(chat_id=call.from_user.id,
                               text=f"Отчет по объекту {object.name} \n"
                                    f"Дата: {report.date} \n"
                                    f" {report.text}",
                               reply_to_message_id=id.message_id)
