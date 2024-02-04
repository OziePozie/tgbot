import asyncio
from config import bot, dp
import logging

from handlers.user.routers import user_router
from handlers.admin.main import router as admin_router


async def main():
    logging.basicConfig(
        level=logging.INFO
    )
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(admin_router)
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
