import json
import os

from datetime import datetime
from bot import bot, database
from aiogram import types
from aiogram.types import InlineKeyboardButton


def check_user(callback):
    user = database["users"].find_one({"telegram_id": callback.from_user.id})

    if not user:
        try:
            database["users"].insert_one({
                "telegram_id": callback.from_user.id,
                "first_name": callback.from_user.first_name,
                "last_name": callback.from_user.last_name,
                "lang_code": callback.from_user.language_code,
                "admin": False,
                "timestamp": round(datetime.now().timestamp())
            })
        except Exception as error:
            print(error)
    else:
        database["users"].update_one(
            {"telegram_id": callback.from_user.id},
            {"$set": {
                "first_name": callback.from_user.first_name,
                "last_name": callback.from_user.last_name
            }}
        )


def get_lang(telegram_id):
    with open("config.json") as config_data:
        config_data = json.load(config_data)

    user = database["users"].find_one({"telegram_id": telegram_id})

    if user:
        languages_list = config_data["bot"]["languages_list"]
        user_lang_file = languages_list.get(user["lang_code"])
        user_lang_file_path = config_data["bot"]["languages_folder"] + user_lang_file

        if os.path.exists(user_lang_file_path):
            with open(user_lang_file_path) as lang_file:
                lang_file = json.load(lang_file)
        else:
            default_user_lang_file_path = config_data["bot"]["languages_folder"] + languages_list.get("en")
            with open(default_user_lang_file_path) as lang_file:
                lang_file = json.load(lang_file)

        return lang_file
    return


async def send_message(callback, text, keyboard: types.InlineKeyboardMarkup = None, parse_mode: str = None):
    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode
        )
        return callback.message.message_id
    except AttributeError:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode
        )


def new_service_info(lang_data, service_id):
    service = database["services"].find_one({"_id": service_id})

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    buttons = {
        "service_name": InlineKeyboardButton(text=lang_data["buttons"]["enter_service_name"], callback_data=f"enter_service_name_{service['_id']}"),
        "service_description": InlineKeyboardButton(text=lang_data["buttons"]["enter_service_description"], callback_data=f"enter_service_description_{service['_id']}"),
        "service_price": InlineKeyboardButton(text=lang_data["buttons"]["enter_service_price"], callback_data=f"enter_service_price_{service['_id']}")
    }

    row = []
    for key in buttons:
        if service[key] is None:
            row.append(buttons[key])
            if len(row) == 2:
                keyboard.inline_keyboard.append(row)
                row = []

    if row:
        keyboard.inline_keyboard.append(row)

    keyboard.inline_keyboard.append([
        types.InlineKeyboardButton(text=lang_data["buttons"]["add_service"], callback_data=f"add_service_{service['_id']}"),
        types.InlineKeyboardButton(text=lang_data["buttons"]["cancel"], callback_data=f"cancel_add_service_{service['_id']}")
    ])

    if service["service_price"] is not None:
        service["service_price"] = format_price(service["service_price"])

    for key in service:
        if service[key] is None:
            service[key] = "Не указано"

    services_text = lang_data["messages"]["info"]["new_service"]
    services_text = services_text.replace("{service_name}", service["service_name"])
    services_text = services_text.replace("{service_description}", service["service_description"])
    services_text = services_text.replace("{service_price}", service["service_price"])

    return services_text, keyboard


def format_price(price):
    if len(price) == 1:
        return f"{price[0]}$"
    else:
        return f"от {price[0]}$ до {price[1]}$"

