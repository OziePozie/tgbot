import datetime
import aioschedule
import asyncio
from config import bot


async def send_message():
    await bot.send_message()

aioschedule.every(15).days.at().do(send_message)


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

# Run the scheduler
try:
    asyncio.run(scheduler())
except KeyboardInterrupt:
    print("Scheduler stopped manually")