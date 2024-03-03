from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import types

from bot import bot, dp, Session


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    from bot.models import Users

    with Session() as session_db:
        user = session_db.query(Users).filter_by(telegram_id=message.from_user.id).first()
        
        if not user:
            session_db.add(Users(
                telegram_id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                lang_code=message.from_user.language_code
            ))
            session_db.commit()

    await bot.send_message(
        chat_id=message.from_user.id,
        text="пошёл нахуй",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
            ],
            [
                types.InlineKeyboardButton(text="Сменить язык", callback_data="change_lang")
            ]
        ])
    )