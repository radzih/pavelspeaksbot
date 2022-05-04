from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.inline import start_test_markup

async def user_start(message: Message) -> None:
    await message.answer(
        text="Hello, user!",
        reply_markup=start_test_markup)



def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
