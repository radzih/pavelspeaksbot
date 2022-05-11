import operator

from aiogram_dialog.widgets.kbd import Button, ScrollingGroup
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Multiselect
from aiogram_dialog.widgets.text import Const, Format

from tgbot.widgets.getters import get_films_categories, get_words_categories
from tgbot.widgets.states import FilmCategories, WordCategories
from tgbot.handlers.choose_categories import add_or_remove_film_category,\
    add_or_remove_word_category, hide_film_category_list,\
    hide_word_category_list


select_words_categories_window = Window(
    Const("Выберите категории для слов"),
    ScrollingGroup(
        Multiselect(
            checked_text=Format('✓ {item[0]}'),
            unchecked_text=Format('{item[0]}'),
            id='multiselect_words_categories',
            item_id_getter=operator.itemgetter(1),
            items="categories",
            on_click=add_or_remove_word_category,
        ),
        id='scr_group_words_categories',
        width=1,
        height=7,
    ),
    Button(
        Const('Закончить выбор категорий'),
        id='hide_choose_category_list',
        on_click=hide_word_category_list,
    ),
    getter=get_words_categories,
    state=WordCategories.choose,
)

select_films_categories_window = Window(
    Const("Выберите категории для фильмов"),
    ScrollingGroup(
        Multiselect(
            checked_text=Format('✓ {item[0]}'),
            unchecked_text=Format('{item[0]}'),
            id='multiselect_films_categories',
            item_id_getter=operator.itemgetter(1),
            items="categories",
            on_click=add_or_remove_film_category,
        ),
        id='scr_group_films_categories',
        width=1,
        height=7,
    ),
    Button(
        Const('Закончить выбор категорий'),
        id='hide_choose_category_list',
        on_click=hide_film_category_list,
    ),
    getter=get_films_categories,
    state=FilmCategories.choose,
)
