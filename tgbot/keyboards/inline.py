from aiogram.types.inline_keyboard import \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

start_test_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Начать тест',
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

profile_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Выбрать категори слов заново',
                callback_data='choose_words_categories'
            )
        ],
        [
            InlineKeyboardButton(
                text='Выбрать категори фильмов заново',
                callback_data='choose_films_categories'
            )
        ],
        [
            InlineKeyboardButton(
                text='Поменять часовой пояс',
                switch_inline_query_current_chat=''
                
            )
        ]
    ]
)

timezone_callback = CallbackData('timezone', 'timezone')
async def confirm_change_timezone_markup(
    timezone: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Да',
                    callback_data=timezone_callback.new(
                        timezone=timezone
                    )
                )
            ]
        ]
    )    

async def watch_film_markup(link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Смотреть🎥',
                    url=link,

                )
            ]
        ]
    )