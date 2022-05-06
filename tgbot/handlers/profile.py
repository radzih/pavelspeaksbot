from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

from tgbot.filters.registered import IsRegistered
from tgbot.services.db import db_get_user_info
from tgbot.keyboards.inline import profile_markup

async def show_profile(
    message: Message) -> None:
    _, user_level, _, user_words_categories = await db_get_user_info(
        telegram_id=message.from_user.id
    )
    text=[
            f'{message.from_user.full_name}\n',
            f'Уровень английского:\n',
            f'<b>{user_level.level}</b>\n',
    ]
    if len(user_words_categories) != 0:
        text.append(
            f'Выбраные категории слов:\n',
        )
        text.append(
            '\n  - '.join(
                cat.category.capitalize() for cat in user_words_categories
                )
            )
    await message.answer(
        text=''.join(text),
        reply_markup=profile_markup,
    )

def register_profile_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        show_profile,
        IsRegistered(),
        commands=['profile']
    )