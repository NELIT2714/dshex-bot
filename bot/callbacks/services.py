from aiogram import types
from aiogram.filters import Command

from bot import dp, database
from bot.functions import get_lang, format_price
from bot.functions import send_message, check_user


@dp.callback_query(lambda query: query.data in ["services", "back_to_services"])
async def services_callback(callback_query: types.CallbackQuery):
    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    user = database["users"].find_one({"telegram_id": callback_query.from_user.id})
    services_list = database["services"].find({"hidden": False})

    services_text = ""
    row = []

    for service in services_list:
        service_str = lang_data["messages"]["templates"]["service"].replace("{service_id}", str(service["_id"]))
        service_str = service_str.replace("{service_name}", service["service_name"])
        service_str = service_str.replace("{service_price}", format_price(service["service_price"]))

        services_text += f"{service_str}\n"

        if len(row) == 4:
            keyboard.inline_keyboard.append(row)
            row = []

        row.append(types.InlineKeyboardButton(text="#" + str(service["_id"]), callback_data="s1"))

    if row:
        keyboard.inline_keyboard.append(row)

    if user["admin"]:
        keyboard.inline_keyboard.append([
            types.InlineKeyboardButton(text=lang_data["buttons"]["add_service"], callback_data="add_service")
        ])

    keyboard.inline_keyboard.append([
        types.InlineKeyboardButton(text=lang_data["buttons"]["back"], callback_data="back_main")
    ])

    await send_message(
        callback=callback_query,
        text=f"Услуги\n\n{services_text}",
        keyboard=keyboard
    )
