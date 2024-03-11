import json
import logging
import pymongo

from aiogram import Dispatcher, Bot

with open("config.json") as config:
    config = json.load(config)

TOKEN = config["bot"]["token"]

bot = Bot(token=TOKEN)
dp = Dispatcher()

db_host, db_user, db_password, db_port, database = config["database"]["host"], config["database"]["user"], config["database"]["password"], config["database"]["port"], config["database"]["database"]

client = pymongo.MongoClient(f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}")
database = client[database]


async def run_bot():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


from bot.commands import start, db
from bot.callbacks import main_menu, services, admin
# , , portfolio, info, my_orders,