from aiogram import types
from aiogram.filters import Command

from bot import dp, Session
from bot.functions import get_lang
from bot.functions import send_message, check_user


@dp.message(Command("menu"))
@dp.callback_query(lambda query: query.data in ["main_menu", "back_main"])
async def main_menu_callback(callback_query: types.CallbackQuery) -> None:
    from bot.models import Users

    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    with Session() as session_db:
        user = session_db.query(Users).filter_by(telegram_id=callback_query.from_user.id).first()

    await send_message(
        callback=callback_query,
        text=lang_data["messages"]["info"]["main_menu"].replace("{user}", user.first_name),
        keyboard=types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["services"], callback_data="services"),
                types.InlineKeyboardButton(text=lang_data["buttons"]["portfolio"], callback_data="portfolio")
            ],
            [
                types.InlineKeyboardButton(text=lang_data["buttons"]["info"], callback_data="info"),
                types.InlineKeyboardButton(text=lang_data["buttons"]["my_orders"], callback_data="my_orders")
            ]
        ])
    )
