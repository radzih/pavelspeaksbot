from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

async def send_bot_info(message: Message) -> None:
    await message.answer(
        text=(
            '🇺🇸Бот, который научит тебя английскому за 3 месяца\n' 
            '✅Выполняй ежедневные задания среди который\n'
            '- новые слова по интересам с картинками и озвучкой\n'
            '- англоязычные видео с YouTube\n'
            '- мотивация от создателя бота\n'
            '- фильмы на выходным\n'
            '- проверочные тесты\n'
        )
    )


def register_info_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        send_bot_info,
        commands=['info'],
    )