import pytz
import sys

from aiogram import Bot
from aiogram.types.input_file import InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.services.db import db_get_random_word


async def scheduler_send_words(
    bot: Bot,
    telegram_id: int) -> None:
    random_word = await db_get_random_word(
        telegram_id=telegram_id
    )
    await bot.send_voice(
        chat_id=telegram_id,
        voice=InputFile(
            path_or_bytesio=f'{sys.path[-1]}{random_word.audio_path}'
        )
    )
    await bot.send_message(
        chat_id=telegram_id,
        text=(
            f'<b>{random_word.word.capitalize()}'
            f'-{random_word.translate.capitalize()}</b>'
            )
    )

async def add_regular_jobs(
    scheduler: AsyncIOScheduler,
    bot: Bot,
    telegram_id: int) -> None:
    for _ in range(5):
        await scheduler_send_words(
            bot=bot,
            telegram_id=telegram_id,
        )

    scheduler.add_job(
        scheduler_send_words,
        id=f'{telegram_id}scheduler_send_words',
        trigger='cron',
        day_of_week='*',
        hour='9, 12, 14, 16, 18',
        timezone=pytz.timezone('Europe/Moscow'),
        kwargs={
            'telegram_id': telegram_id,
            },
        jitter=3000,
    )