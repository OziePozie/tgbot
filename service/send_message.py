import asyncio
from datetime import datetime, timedelta
from config import db_session, bot
from data.models import Transports


async def send_message(user_id):
    current_date = datetime.now().date()

    await bot.send_message(chat_id=user_id, text="Необходимо указать пробег авто")

    transport = db_session.query(Transports).filter(Transports.master_id == user_id).first()

    if transport:
        update_date = current_date
        next_message = current_date + timedelta(days=15)

        next_message_formatted = next_message.strftime("%d.%m.%Y")

        transport.next_message = next_message_formatted

        db_session.commit()


async def scheduler():
    while True:
        current_date = datetime.now().date().strftime("%d.%m.%Y")

        date_from_db = db_session.query(Transports.next_message, Transports.master_id).all()
        for data in date_from_db:
            date_obj = datetime.strptime(data[0], "%d.%m.%Y")

            date_formated = datetime.strftime(date_obj, "%d.%m.%Y")

            if current_date == date_formated:
                await send_message(int(data[1]))
            else:
                pass
        await asyncio.sleep(10)
