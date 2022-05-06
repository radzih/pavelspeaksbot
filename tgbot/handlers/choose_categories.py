from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Multiselect
from aiogram.dispatcher import Dispatcher

from tgbot.services.db import db_add_user_word_category,\
     db_delete_categories, db_get_user_info,\
        db_remove_user_word_category
from tgbot.widgets.states import ChooseCategories



async def add_or_remove_category(
    call: CallbackQuery, 
    multiselect: Multiselect,
    dialog_manager: DialogManager,
    category_id: int) -> None:
    if category_id not in multiselect.get_checked():
        await db_add_user_word_category(
            telegram_id=call.from_user.id,
            category_id=category_id,
        )
    else:
        await db_remove_user_word_category(
            telegram_id=call.from_user.id,
            category_id=category_id,
        )

async def hide_choose_category_list(
    call: CallbackQuery,
    *args) -> None:
    *_, user_words_categories = await db_get_user_info(
        telegram_id=call.from_user.id
    )
    if len(user_words_categories) > 2:
        await call.message.edit_text(
            text='Категории добавлены'
        )    
    else:
        await call.answer(
            text='Выберите минимум 3 категории'
        )

async def choose_words_categories(
    call: CallbackQuery,
    dialog_manager: DialogManager) -> None: 
    await call.message.delete()
    await db_delete_categories(
        telegram_id=call.from_user.id
    )
    await dialog_manager.start(
        state=ChooseCategories.words_categories,
        data=call.from_user.id,
        mode=StartMode.RESET_STACK,
    )

def register_choose_categories_handlers(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        choose_words_categories,
        text='choose_words_categories',
    )
