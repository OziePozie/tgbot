from aiogram import types
from keyboard.user.main import main
from aiogram import Router, F
from .autocran import router as autocran_router
from .main import router as main_router
from .performance_report import router as performance_report_router
from .transport import router as transport_router
from .travel_orders import router as travel_orders_router
from .living import router as living_router
from .other_expenses import router as other_expenses_router
from .update_km import router as update_km_router

user_router = Router()

user_router.include_router(autocran_router)
user_router.include_router(main_router)
user_router.include_router(performance_report_router)
user_router.include_router(transport_router)
user_router.include_router(travel_orders_router)
user_router.include_router(living_router)
user_router.include_router(other_expenses_router)
user_router.include_router(update_km_router)


@user_router.callback_query(F.data == "back_menu")
async def back(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню", reply_markup=main())
