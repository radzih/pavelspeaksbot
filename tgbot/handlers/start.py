from aiogram import Dispatcher
from aiogram.types import Message
from aiogram_dialog import DialogManager
from tgbot.filters.notregistered import NotRegistered

from tgbot.keyboards.inline import start_test_markup
from tgbot.widgets.states import ChooseCategories

async def user_start(message: Message) -> None:
    await message.answer(
        text="Hello, user!",
        reply_markup=start_test_markup)

async def say_that_bot_already_started(
    message: Message) -> None:
    await message.asnwer(
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

    
