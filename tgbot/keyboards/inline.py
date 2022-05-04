from aiogram.types.inline_keyboard import \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

start_test_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Start test',
                callback_data='start_test',
            )
        ]
    ]
)

answer_callback_data = CallbackData('answer', 'answer')

async def get_answers_markup(
    answers: list) -> InlineKeyboardMarkup:
    answer_kb = InlineKeyboardMarkup()
    for answer in answers:
        answer_kb.add(
            InlineKeyboardButton(
                text=answer,
                callback_data=answer_callback_data.new(
                    answer=answer
                )
            )
        )
    return answer_kb