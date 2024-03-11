from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types

from bot import bot, dp, database


@dp.message(Command("db"))
async def db_cmd(message: Message) -> None:
    for coll in database.list_collection_names():
        database.drop_collection(coll)
        database.create_collection(coll)

        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Коллекция {coll} пересоздана"
        )

    await bot.send_message(
        chat_id=message.from_user.id,
        text="Пересоздание коллекций завершено!"
    )
