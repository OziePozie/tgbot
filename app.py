import asyncio
from config import bot, dp
import logging
<<<<<<< HEAD
from handlers.user.main import router
from handlers.admin.main import router as admin_router
=======
from handlers.user.main import router as main_router
from handlers.user.level2 import router as level_2_router
>>>>>>> 3eca0f5b36613412590b85855d64c393c86f0d34


async def main():
    logging.basicConfig(
        level=logging.INFO
    )
    await bot.delete_webhook(drop_pending_updates=True)
<<<<<<< HEAD
    dp.include_router(router)
    dp.include_router(admin_router)

=======
    dp.include_router(main_router)
    dp.include_router(level_2_router)
>>>>>>> 3eca0f5b36613412590b85855d64c393c86f0d34
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
