from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
import pytz

from tgbot.services.db import db_get_random_word


async def scheduler_send_words(
    bot: Bot,
    telegram_id: int) -> None:
    random_word = await db_get_random_word(
        telegram_id=telegram_id
    )

async def add_regular_jobs(
    scheduler: AsyncIOScheduler,
    telegram_id: int) -> None:
    scheduler.add_job(
        scheduler_send_words,
        'cron',
        hour='9 12 14 16 18',
        timezone=pytz.timezone('Europe/Moscow'),
        jitter=3000,
    )