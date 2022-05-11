import pytz

from aiogram import Bot
from aiogram.types.input_file import InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.keyboards.inline import watch_film_markup
from tgbot.services.db import db_get_random_film,\
    db_get_random_tip, db_get_random_word


async def send_word(
    bot: Bot,
    telegram_id: int) -> None:
    random_word = await db_get_random_word(
        telegram_id=telegram_id
    )
    await bot.send_voice(
        chat_id=telegram_id,
        voice=InputFile(
            path_or_bytesio=f'.{random_word.audio_path}'
        )
    )
    await bot.send_message(
        chat_id=telegram_id,
        text=(
            f'<b>{random_word.word.capitalize()} '
            f'- {random_word.translate.capitalize()}</b>\n'
            f'👆Вот и новое слово, обязательно выучи его'
            )
    )

async def send_film(
    bot: Bot,
    telegram_id: int) -> None:
    random_film = await db_get_random_film(
        telegram_id=telegram_id
    )
    await bot.send_message(
        chat_id=telegram_id,
        text=(
            f'<b>Рекомендую посмотреть фильм</b>\n'
            f'<b>{random_film.original_name}</b>'
            f'<a href="{random_film.link}">⠀</a>'
            ),
        reply_markup=await watch_film_markup(random_film.link),
    )

async def send_tip(
    bot: Bot,
    telegram_id: int) -> None:
    random_tip = await db_get_random_tip(
        telegram_id=telegram_id
    )
    await bot.send_voice(
        chat_id=telegram_id,
        voice=InputFile(
            path_or_bytesio=random_tip.audio_path
        ),
        caption='👆Совет от создателя бота👆', 
    )

async def add_jobs(
    scheduler: AsyncIOScheduler,
    bot: Bot,
    telegram_id: int) -> None:
    SEND_WORD_ON_START = 5
    for _ in range(SEND_WORD_ON_START):
        await send_word(
            bot=bot,
            telegram_id=telegram_id,
        )

    scheduler.add_job(
        send_word,
        id=f'{telegram_id}send_word',
        trigger='cron',
        day_of_week='*',
        hour='9, 12, 14, 16, 18',
        timezone=pytz.timezone('Europe/Moscow'),
        kwargs={
            'telegram_id': telegram_id,
            },
        jitter=3000,
    )
    scheduler.add_job(
        send_film,
        id=f'{telegram_id}send_film',
        trigger='cron',
        day_of_week='fri',
        hour='16',
        timezone=pytz.timezone('Europe/Moscow'),
        kwargs={
            'telegram_id': telegram_id,
            },
        jitter=5000,
    )
    scheduler.add_job(
        send_tip,
        id=f'{telegram_id}send_tip',
        trigger='interval',
        days=3,
        kwargs={
            'telegram_id': telegram_id,
            },
        jitter=10000,
    )
