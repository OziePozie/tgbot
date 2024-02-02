import asyncio

from config import bot, dp
import logging
from handlers.user.main import router


async def main():
    logging.basicConfig(
        level=logging.INFO
    )
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
