import sys

from aiogram.dispatcher import Dispatcher
from aiogram.types import Message
from aiogram.types.input_file import InputFile

from tgbot.filters.registered import IsRegistered
from tgbot.services.db import db_get_user_words

async def repeat_words(message: Message) -> None:
    user_words = await db_get_user_words(
        telegram_id=message.from_user.id
    )
    for word in user_words[:5]:
        await message.bot.send_voice(
            chat_id=message.from_user.id,
            voice=InputFile(
                path_or_bytesio=f'{sys.path[-1]}{word.audio_path}'
            )
        )
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=(
                f'<b>{word.word.capitalize()} '
                f'- {word.translate.capitalize()}</b>'
                )
        )


def register_repeat_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        repeat_words,
        IsRegistered(),
        commands=['repeat'],

    )