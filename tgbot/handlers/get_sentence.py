import random

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, ContentType

GOOD_ANSWERS = [
    'Молодец, так держать',
    'Отлично сделано',
    'Продолжай в том же духе',
    'Here we go',
    'Поздравляю, ты справился',
    'Good sentence',
    'Excelent pronunciation',
]

BAD_ANSWERS = [
    '😡 Нужно было составить предложение!!!',
    'Ну я же сказал сделать предложение, почему не слушаешь?',
    'Оу, нужно было сделать',
    'Почему не слушаемся?',
]

async def say_good(message: Message, state: FSMContext) -> None:
    await message.answer(text=random.choice(GOOD_ANSWERS))
    await state.finish()

async def say_bad(bot: Message, telegram_id: int) -> None:
    await bot.send_message(
            chat_id=telegram_id,
            text=random.choice(BAD_ANSWERS)
        )

async def say_that_user_must_make_sentence(message: Message):
    await message.answer('Сначала сочините предложение, и скиньте головое')
 
def register_get_sentence_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        say_good,
        content_types=ContentType.VOICE,
        state='get_voice'
    )
    dp.register_message_handler(
        say_that_user_must_make_sentence,
        state='get_voice'
    )