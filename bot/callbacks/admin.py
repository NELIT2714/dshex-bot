import re

import pymongo
from aiogram import types
from aiogram.filters import Command

from bot import dp, bot, database
from bot.callbacks.main_menu import main_menu_callback
from bot.functions import get_lang, send_message, check_user, new_service_info
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class NewService(StatesGroup):
    service_name = State()
    service_description = State()
    service_price = State()


@dp.callback_query(lambda query: query.data == "add_service")
async def add_service_callback(callback_query: types.CallbackQuery):
    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    user = database["users"].find_one({"telegram_id": callback_query.from_user.id})

    if user["admin"]:
        try:
            max_id = database["services"].find_one(sort=[("_id", pymongo.DESCENDING)])["_id"]
        except:
            max_id = None

        new_service = database["services"].insert_one({
            "_id": max_id + 1 if max_id else 1,
            "service_name": None,
            "service_description": None,
            "service_price": None,
            "hidden": True
        })

        services_text, keyboard = new_service_info(lang_data, new_service.inserted_id)

        new_service_message = await send_message(
            callback=callback_query,
            text=services_text,
            keyboard=keyboard,
            parse_mode="html"
        )

        database["temp"].insert_one({
            "chat_id": callback_query.from_user.id,
            "message_id": new_service_message,
            "service_id": new_service.inserted_id,
            "hint": "new_service_message"
        })


# Добавление названия услуги
@dp.callback_query(lambda query: query.data.startswith("enter_service_name_"))
async def enter_service_name_callback(callback_query: types.CallbackQuery, state: FSMContext):
    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    user = database["users"].find_one({"telegram_id": callback_query.from_user.id})
    service_id = callback_query.data.split("_")[-1]

    if user["admin"]:
        service = database["services"].find_one({"_id": int(service_id)})

        if service is not None:
            enter_service_name_message = await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=lang_data["messages"]["info"]["send_service_name"]
            )
            database["temp"].insert_one({
                "chat_id": callback_query.from_user.id,
                "message_id": enter_service_name_message.message_id,
                "service_id": service["_id"],
                "hint": "enter_service_name_message"
            })
            await callback_query.answer()
            await state.set_state(NewService.service_name)


# Добавление описания услуги
@dp.callback_query(lambda query: query.data.startswith("enter_service_description_"))
async def enter_service_name_callback(callback_query: types.CallbackQuery, state: FSMContext):
    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    user = database["users"].find_one({"telegram_id": callback_query.from_user.id})
    service_id = callback_query.data.split("_")[-1]

    if user["admin"]:
        service = database["services"].find_one({"_id": int(service_id)})

        if service is not None:
            enter_service_desc_message = await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=lang_data["messages"]["info"]["send_service_description"]
            )
            database["temp"].insert_one({
                "chat_id": callback_query.from_user.id,
                "message_id": enter_service_desc_message.message_id,
                "service_id": service["_id"],
                "hint": "enter_service_desc_message"
            })
            await callback_query.answer()
            await state.set_state(NewService.service_description)


# Добавление цены услуги
@dp.callback_query(lambda query: query.data.startswith("enter_service_price_"))
async def enter_service_price_callback(callback_query: types.CallbackQuery, state: FSMContext):
    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    user = database["users"].find_one({"telegram_id": callback_query.from_user.id})
    service_id = callback_query.data.split("_")[-1]

    if user["admin"]:
        service = database["services"].find_one({"_id": int(service_id)})

        if service is not None:
            enter_service_price_message = await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=lang_data["messages"]["info"]["send_service_price"]
            )
            database["temp"].insert_one({
                "chat_id": callback_query.from_user.id,
                "message_id": enter_service_price_message.message_id,
                "service_id": service["_id"],
                "hint": "enter_service_price_message"
            })
            await callback_query.answer()
            await state.set_state(NewService.service_price)


# Добавление услуги
@dp.callback_query(lambda query: query.data.startswith("add_service_"))
async def add_service_button(callback_query: types.CallbackQuery):
    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    user = database["users"].find_one({"telegram_id": callback_query.from_user.id})
    service_id = callback_query.data.split("_")[-1]

    if user["admin"]:
        database["services"].update_one(
            {"_id": int(service_id)},
            {"$set": {
                "hidden": False
            }}
        )
        await callback_query.message.edit_text(
            text=lang_data["messages"]["info"]["service_was_created"],
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=lang_data["buttons"]["back"], callback_data="back_to_services")
                ]
            ])
        )


# Отмена добавления услуги
@dp.callback_query(lambda query: query.data.startswith("cancel_add_service_"))
async def cancel_add_service(callback_query: types.CallbackQuery):
    check_user(callback_query)

    user = database["users"].find_one({"telegram_id": callback_query.from_user.id})
    service_id = callback_query.data.split("_")[-1]

    if user["admin"]:
        service = database["services"].find_one({"_id": int(service_id)})
        database["services"].delete_one({"_id": service["_id"]})
        await main_menu_callback(callback_query)


@dp.message(NewService.service_name)
async def add_service_name(message: types.Message):
    check_user(message)
    lang_data = get_lang(message.from_user.id)

    new_service_message = database["temp"].find_one({"chat_id": message.from_user.id, "hint": "new_service_message"}, sort=[("_id", pymongo.DESCENDING)])
    enter_service_name_message = database["temp"].find_one({"chat_id": message.from_user.id, "hint": "enter_service_name_message"}, sort=[("_id", pymongo.DESCENDING)])

    database["services"].update_one(
        {"_id": new_service_message["service_id"]},
        {"$set": {
            "service_name": message.text
        }}
    )

    services_text, keyboard = new_service_info(lang_data, new_service_message["service_id"])

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=new_service_message["message_id"],
        text=services_text,
        reply_markup=keyboard,
        parse_mode="html"
    )
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=enter_service_name_message["message_id"])


@dp.message(NewService.service_description)
async def add_service_description(message: types.Message):
    check_user(message)
    lang_data = get_lang(message.from_user.id)

    new_service_message = database["temp"].find_one({"chat_id": message.from_user.id, "hint": "new_service_message"}, sort=[("_id", pymongo.DESCENDING)])
    enter_service_desc_message = database["temp"].find_one({"chat_id": message.from_user.id, "hint": "enter_service_desc_message"}, sort=[("_id", pymongo.DESCENDING)])

    database["services"].update_one(
        {"_id": new_service_message["service_id"]},
        {"$set": {
            "service_description": message.text
        }}
    )

    services_text, keyboard = new_service_info(lang_data, new_service_message["service_id"])

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=new_service_message["message_id"],
        text=services_text,
        reply_markup=keyboard,
        parse_mode="html"
    )
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=enter_service_desc_message["message_id"])


@dp.message(NewService.service_price)
async def add_service_price(message: types.Message):
    check_user(message)
    lang_data = get_lang(message.from_user.id)

    new_service_message = database["temp"].find_one({"chat_id": message.from_user.id, "hint": "new_service_message"}, sort=[("_id", pymongo.DESCENDING)])
    enter_service_price_message = database["temp"].find_one({"chat_id": message.from_user.id, "hint": "enter_service_price_message"}, sort=[("_id", pymongo.DESCENDING)])

    pattern = r"(\d+(?:[,.]\d+)?)\s*([-–—]\s*(\d+(?:[,.]\d+)?)?)?"
    matches = re.findall(pattern, message.text)
    price = ()

    for match in matches:
        price_from = float(match[0].replace(',', '.'))

        if match[-1]:
            price_to = float(match[-1].replace(',', '.'))
            if price_from < price_to:
                price += (price_from, price_to)
            else:
                await message.reply(lang_data["messages"]["errors"]["price_error"])
        else:
            price += (price_from,)

    database["services"].update_one(
        {"_id": new_service_message["service_id"]},
        {"$set": {
            "service_price": price
        }}
    )

    services_text, keyboard = new_service_info(lang_data, new_service_message["service_id"])

    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=new_service_message["message_id"],
        text=services_text,
        reply_markup=keyboard,
        parse_mode="html"
    )
    await message.delete()
    await bot.delete_message(chat_id=message.from_user.id, message_id=enter_service_price_message["message_id"])
