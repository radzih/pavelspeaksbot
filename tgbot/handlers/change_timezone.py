import pytz

from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineQuery,\
    InlineQueryResultArticle, InputMessageContent,\
        Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.filters.istimezone import IsTimezone
from tgbot.keyboards.inline import confirm_change_timezone_markup,\
    timezone_callback


async def select_timezone(query: InlineQuery) -> None:
    results = []
    for i, timezone in enumerate(pytz.all_timezones):
        if query.query.lower() in timezone.lower():
            results.append(
                InlineQueryResultArticle(
                    id=i,
                    title=timezone,
                    input_message_content=InputMessageContent(
                        message_text=timezone
                    )
                )
            )
        if len(results) == 50:
            break
    await query.answer(results=results)

async def confirm_changing_timezone(message: Message) -> None:
    await message.answer(
        text=(
            'Вы уверненны что хотите поменять часовой пояс на \n'
            f'           <b>{message.text}</b>                ' 
        ),
        reply_markup=await confirm_change_timezone_markup(
            timezone=message.text
        )
    )

async def change_timezone(
    call: CallbackQuery,
    scheduler: AsyncIOScheduler,
    callback_data: dict) -> None:
    scheduler.modify_job(
        job_id=f"{call.from_user.id}send_word",
        timezone=pytz.timezone(callback_data['timezone'])
    )
    await call.message.edit_text(
        text='Часовой пояс смёнен'
    )


def register_change_timezone_handlers(dp: Dispatcher) -> None:
    dp.register_inline_handler(
        select_timezone,
    )
    dp.register_message_handler(
        confirm_changing_timezone,
        IsTimezone(),
    )
    dp.register_callback_query_handler(
        change_timezone,
        timezone_callback.filter(),
    )

