from aiogram_dialog import Dialog

from tgbot.widgets.windows import select_words_categories_window,\
    select_films_categories_window

words_categories_dialog = Dialog(select_words_categories_window)
films_categories_dialog = Dialog(select_films_categories_window)