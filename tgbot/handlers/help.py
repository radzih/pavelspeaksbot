from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

async def send_help(message: Message) -> None:
    await message.answer(
        text=(
            '/profile - показывает профиль\n'
            '/repeat - повторить 5 выученых слов\n'
            '/help - показывает команды\n'
            '/info - для чего этот бот\n'
        )
    )


def register_help_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        send_help,
        commands=['help'],
    )