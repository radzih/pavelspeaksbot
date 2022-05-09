import pytz

from aiogram import Bot
from aiogram_dialog import DialogRegistry
from aiogram.types.input_file import InputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram_dialog.manager.bg_manager import BgManager

from tgbot.services.db import db_get_random_tip, db_get_random_word
from tgbot.widgets.states import ChooseCategories


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
            f'- {random_word.translate.capitalize()}</b>'
            )
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

async def choose_words_categories(
    telegram_id: int,
    bot: Bot,
    registry: DialogRegistry) -> None:
    chat_member_object = await bot.get_chat_member(
        chat_id=telegram_id,
        user_id=telegram_id,
        )
    chat_object = await bot.get_chat(
        chat_id=telegram_id,
        )
    bg_manager = BgManager(
        user = chat_member_object.user,
        chat = chat_object,
        bot = bot,
        registry = registry,
        stack_id = '',
        intent_id = None
    )
    await bg_manager.start(
        state=ChooseCategories.words_categories,
        data=telegram_id,
    )

async def add_jobs(
    scheduler: AsyncIOScheduler,
    bot: Bot,
    telegram_id: int) -> None:
    for _ in range(5):
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
        send_tip,
        id=f'{telegram_id}send_tip',
        trigger='cron',
        day_of_week='mon, wed, fri',
        hour='14',
        timezone=pytz.timezone('Europe/Moscow'),
        kwargs={
            'telegram_id': telegram_id,
            },
        jitter=6000,
    )
    scheduler.add_job(
        choose_words_categories,
        id=f'{telegram_id}choose_words_categories',
        trigger='date',
        run_date=pytz.datetime.datetime.now() + pytz.datetime.timedelta(days=1),
        kwargs={
            'telegram_id': telegram_id,
            },
    )
