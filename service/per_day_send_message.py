import asyncio
from datetime import datetime, timedelta
from config import db_session, bot
from data.models import PerformanceReport


async def send_message(user_id):
    current_date = datetime.now().date()

    await bot.send_message(chat_id=user_id, text="Необходимо заполнить отчет")

    report = db_session.query(PerformanceReport).filter(PerformanceReport.user_id == user_id).first()

    if report:
        update_date = current_date
        next_message = current_date + timedelta(days=1)

        next_message_formatted = next_message.strftime("%d.%m.%Y")

        report.date = next_message_formatted
        report.is_sendReport = False

        db_session.commit()


async def scheduler_per_day():
    while True:
        current_date = datetime.now().date().strftime("%d.%m.%Y")

        date_from_db = db_session.query(PerformanceReport.is_sendReport, PerformanceReport.user_id,
                                        PerformanceReport.date).all()
        for data in date_from_db:
            date_obj = datetime.strptime(data[2], "%d.%m.%Y")

            date_formated = datetime.strftime(date_obj, "%d.%m.%Y")

            if current_date == date_formated and data[0] is False:
                await send_message(int(data[1]))
            else:
                pass
        await asyncio.sleep(43200)
