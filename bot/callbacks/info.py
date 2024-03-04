from aiogram import types
from aiogram.filters import Command

from bot import dp, Session
from bot.functions import get_lang
from bot.functions import send_message, check_user


@dp.callback_query(lambda query: query.data == "info")
async def services_callback(callback_query: types.CallbackQuery):
    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    await send_message(
        callback=callback_query,
        text="Инфа Маши",
        keyboard=types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["back"], callback_data="back_main")
            ]
        ])
    )
