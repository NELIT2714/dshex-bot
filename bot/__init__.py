import json
import logging

from aiogram import Dispatcher, Bot

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("config.json") as config:
    config = json.load(config)

TOKEN = config["bot"]["token"]

bot = Bot(token=TOKEN)
dp = Dispatcher()

db_host, db_user, db_password, db_port, schema = config["database"]["host"], config["database"]["user"], config["database"]["password"], config["database"]["port"], config["database"]["database"]

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{schema}", pool_pre_ping=True, pool_recycle=3600)
Session = sessionmaker(bind=engine)
Base = declarative_base()

Base.metadata.create_all(engine)


async def run_bot():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


from bot import models
from bot.commands import start, db
# from callbacks import *
