from aiogram import types
from aiogram.filters import Command

from bot import dp, Session, bot
from bot.functions import get_lang, send_message, check_user
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class NewService(StatesGroup):
    service_name = State()
    service_description = State()
    service_price = State()


@dp.callback_query(lambda query: query.data in ["add_service", "cancel_add_service"])
async def add_service_callback(callback_query: types.CallbackQuery, state: FSMContext):
    from bot.models import Users

    check_user(callback_query)
    lang_data = get_lang(callback_query.from_user.id)

    state_data = await state.get_data()

    with Session() as session_db:
        user = session_db.query(Users).filter_by(telegram_id=callback_query.from_user.id).first()

        if callback_query.data == "add_service":

            if user.admin:
                await send_message(
                    callback=callback_query,
                    text=lang_data["messages"]["info"]["new_service"],
                    keyboard=types.InlineKeyboardMarkup(inline_keyboard=[
                        [
                            types.InlineKeyboardButton(text=lang_data["buttons"]["back"], callback_data="cancel_add_service")
                        ]
                    ]),
                    parse_mode="Markdown"
                )
                add_service_name_message = await bot.send_message(
                    chat_id=callback_query.from_user.id,
                    text=lang_data["messages"]["info"]["send_service_name"]
                )
                await state.update_data(add_service_name_message=add_service_name_message.message_id)
                await state.set_state(NewService.service_name)

        elif callback_query.data == "cancel_add_service":

            await state.set_state(None)
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=state_data["add_service_name_message"])
            await send_message(
                callback=callback_query,
                text="хуй"
            )


@dp.message(NewService.service_name)
async def add_service_name(message: types.Message):
    await message.reply(f"ты отправил {message.text}")
