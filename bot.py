import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogRegistry
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.change_timezone import register_change_timezone_handlers
from tgbot.handlers.choose_categories import register_choose_categories_handlers
from tgbot.handlers.help import register_help_handlers
from tgbot.handlers.info import register_info_handlers
from tgbot.handlers.profile import register_profile_handlers
from tgbot.handlers.repeat import register_repeat_handlers
from tgbot.handlers.start import register_start_handlers
from tgbot.handlers.test import register_test_handlers
from tgbot.middlewares.scheduler import SchedulerMiddleware
from tgbot.middlewares.db import DbMiddleware
from tgbot.widgets.dialogs import words_categories_dialog

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, scheduler):
    dp.setup_middleware(DbMiddleware())
    dp.setup_middleware(SchedulerMiddleware(scheduler))

def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_start_handlers(dp)
    register_test_handlers(dp)
    register_repeat_handlers(dp)
    register_info_handlers(dp)
    register_help_handlers(dp)
    register_profile_handlers(dp)
    register_choose_categories_handlers(dp)
    register_change_timezone_handlers(dp)

def register_dialogs(regitry):
    regitry.register(words_categories_dialog)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    job_stores = {
        "default": RedisJobStore(
            host=config.redis.host,
            jobs_key="dispatched_trips_jobs",
            run_times_key="dispatched_trips_running"
        )
    }

    storage = RedisStorage2(
        host=config.redis.host
        ) if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    registry = DialogRegistry(dp)  
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=job_stores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.ctx.add_instance(registry, declared_class=DialogRegistry)


    bot['config'] = config

    register_all_middlewares(dp, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)
    register_dialogs(registry)

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
