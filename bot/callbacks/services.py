from aiogram import types
from aiogram.filters import Command

from bot import dp, Session
from bot.functions import get_lang
from bot.functions import send_message, check_user


@dp.callback_query(lambda query: query.data == "services")
async def services_callback(callback_query: types.CallbackQuery):
    from bot.models import Users

    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])

    with Session() as session_db:
        user = session_db.query(Users).filter_by(telegram_id=callback_query.from_user.id).first()

        if user.admin:
            keyboard.inline_keyboard.append([
                types.InlineKeyboardButton(text=lang_data["buttons"]["add_service"], callback_data="add_service")
            ])

    keyboard.inline_keyboard.append([
        types.InlineKeyboardButton(text=lang_data["buttons"]["back"], callback_data="back_main")
    ])

    await send_message(
        callback=callback_query,
        text="Услуги",
        keyboard=keyboard
    )
