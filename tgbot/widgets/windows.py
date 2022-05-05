import operator

from aiogram_dialog.widgets.kbd import Button, ScrollingGroup
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Multiselect
from aiogram_dialog.widgets.text import Const, Format

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
        ),
        id='scr_group_words_categories',
        width=1,
        height=7,
    ),
    getter=get_words_categories,
    state=ChooseCategories.words_categories,
)

