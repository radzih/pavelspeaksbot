import json


from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import CallbackQuery


from tgbot.services.db import db_add_user, db_get_questions,\
    db_add_user_level
from tgbot.keyboards.inline import get_answers_markup
from tgbot.keyboards.inline import answer_callback_data
from tgbot.filters.notregistered import NotRegistered

async def say_that_test_passed(
    call: CallbackQuery) -> None:
    await call.message.edit_text(
        text='You already passed test'
    )

async def start_test(
    call: CallbackQuery, 
    state: FSMContext) -> None:
    await state.set_state('testing')
    await state.update_data(
        question_num=0,
        points=0

    )

    await db_add_user(
        telegram_id=call.from_user.id
    )

    questions = await db_get_questions()
    question = questions[0].question
    answers = json.loads(questions[0].answers)

    await call.message.edit_text(
        text=question,
        reply_markup=await get_answers_markup(
            answers=answers
        )
    )

async def testing(
    call: CallbackQuery, 
    state: FSMContext,
    callback_data: dict) -> None:
    await call.answer()
    state_data = await state.get_data()
    questions = await db_get_questions()
    
    previous_question_num = state_data.get('question_num')
    points = state_data.get('points')
    answer_to_previous_question = callback_data.get('answer')

    previous_question = questions[previous_question_num]

    if answer_to_previous_question == previous_question.correct_answer:
        points += previous_question.point

    if len(questions) == previous_question_num+1:
        await state.finish()
        await calculate_results(
            call=call,
            points=points,
        )
        return

    await state.update_data(
        points=points,
        question_num=previous_question_num+1,
    )
    next_question = questions[previous_question_num+1]
    await call.message.edit_text(
        text=next_question.question,
        reply_markup=await get_answers_markup(
            answers=json.loads(next_question.answers)
        )
    )

async def calculate_results(
    call: CallbackQuery,
    points: int) -> None:
    level = 'Низкий' if points < 17 else 'Средний' 
    await db_add_user_level(
        user_level=level,
        telegram_id=call.from_user.id
    )
    await call.message.edit_text(
        text=(
            'Вы прошли тест \n'
            f'Ваш уровень английского {level.lower()}\n'
            'Жмите /help'
            )
    )

def register_test_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        testing,
        answer_callback_data.filter(),
        state='testing',
    )
    dp.register_callback_query_handler(
        start_test,
        NotRegistered(),
        text='start_test',
    )
    dp.register_callback_query_handler(
        callback=say_that_test_passed,
        text='start_test',
    )