import telnetlib
from tkinter import Button
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Multiselect

from tgbot.services.db import db_add_user_word_category, db_get_user_words_categories, db_remove_user_word_category



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
    user_words_categories = await db_get_user_words_categories(
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