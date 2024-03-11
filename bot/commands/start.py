from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import types
from bot import bot, dp
from bot.functions import get_lang, check_user


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    check_user(message)
    lang_data = get_lang(message.from_user.id)

    await bot.send_message(
        chat_id=message.from_user.id,
        text=lang_data["messages"]["info"]["start_message"],
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["main_menu"], callback_data="main_menu"),
                types.InlineKeyboardButton(text=lang_data["buttons"]["change_lang"], callback_data="change_lang")
            ]
        ])
    )
