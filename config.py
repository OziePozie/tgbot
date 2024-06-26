import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from data.models import Base

load_dotenv()

admin_login = os.getenv("ADMIN_LOGIN")
admin_password = os.getenv("ADMIN_PASSWORD")


user_password = os.getenv("USER_PASSWORD")

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

engine = create_engine('sqlite:///database.sqlite', echo=False)
Base.metadata.create_all(engine)
db_session = Session(bind=engine)

dp = Dispatcher(bot=bot, storage=MemoryStorage())
