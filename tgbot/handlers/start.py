from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.filters.notregistered import NotRegistered
from tgbot.keyboards.inline import start_test_markup

async def user_start(message: Message) -> None:
    await message.answer(
        text="Привет сначала нужно пройти тест",
        reply_markup=start_test_markup)

async def say_that_bot_already_started(
    message: Message) -> None:
    await message.answer(
        text='Вы уже стартанули бота'
    )

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_start,
        NotRegistered(),
        commands=["start"])
    dp.register_message_handler(
        say_that_bot_already_started, 
        commands=["start"]
        )

    
