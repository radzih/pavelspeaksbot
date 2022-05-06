import operator

from aiogram_dialog.widgets.kbd import Button, ScrollingGroup
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Multiselect
from aiogram_dialog.widgets.text import Const, Format
from tgbot.handlers.choose_categories import add_or_remove_category, hide_choose_category_list

from tgbot.widgets.getters import get_words_categories
from tgbot.widgets.states import ChooseCategories


select_words_categories_window = Window(
    Const("Выберите категории для слов"),
    ScrollingGroup(
        Multiselect(
            checked_text=Format('✓ {item[0]}'),
            unchecked_text=Format('{item[0]}'),
            id='multiselect_words_categories',
            item_id_getter=operator.itemgetter(1),
            items="categories",
            on_click=add_or_remove_category,
        ),
        id='scr_group_words_categories',
        width=1,
        height=7,
    ),
    Button(
        Const('Закончить выбор категорий'),
        id='hide_choose_category_list',
        on_click=hide_choose_category_list,
    ),
    getter=get_words_categories,
    state=ChooseCategories.words_categories,
)

