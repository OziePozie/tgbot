import asyncio
from config import bot, dp
import logging

from handlers.user.main import router as main_router



async def main():
    logging.basicConfig(
        level=logging.INFO
    )
    await bot.delete_webhook(drop_pending_updates=True)


    dp.include_router(main_router)
    dp.include_router(level_2_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
