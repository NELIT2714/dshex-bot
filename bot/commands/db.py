from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import types

from bot import bot, dp, Base, engine


@dp.message(Command("db"))
async def db_cmd(message: Message) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
