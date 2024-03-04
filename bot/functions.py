import json
import os

from bot import bot, Session
from aiogram import types


def check_user(callback):
    from bot.models import Users

    with Session() as session_db:
        user = session_db.query(Users).filter_by(telegram_id=callback.from_user.id).first()

        if not user:
            try:
                session_db.add(Users(
                    telegram_id=callback.from_user.id,
                    first_name=callback.from_user.first_name,
                    last_name=callback.from_user.last_name,
                    lang_code=callback.from_user.language_code
                ))
                session_db.commit()
            except Exception as error:
                print(error)
                session_db.rollback()
        else:
            user.first_name = callback.from_user.first_name
            user.last_name = callback.from_user.last_name


def get_lang(telegram_id):
    from bot.models import Users

    with open("config.json") as config_data:
        config_data = json.load(config_data)

    with Session() as session_db:
        user = session_db.query(Users).filter_by(telegram_id=telegram_id).first()

    languages_list = config_data["bot"]["languages_list"]
    user_lang_file = languages_list.get(user.lang_code)
    user_lang_file_path = config_data["bot"]["languages_folder"] + user_lang_file

    if os.path.exists(user_lang_file_path):
        with open(user_lang_file_path) as lang_file:
            lang_file = json.load(lang_file)
    else:
        default_user_lang_file_path = config_data["bot"]["languages_folder"] + languages_list.get("en")
        with open(default_user_lang_file_path) as lang_file:
            lang_file = json.load(lang_file)

    return lang_file


async def send_message(callback, text, keyboard: types.InlineKeyboardMarkup = None, parse_mode: str = None):
    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode
        )
    except AttributeError:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode
        )
