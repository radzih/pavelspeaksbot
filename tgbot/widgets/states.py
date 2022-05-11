from aiogram.dispatcher.filters.state \
    import StatesGroup, State

class WordCategories(StatesGroup):
    choose = State()

class FilmCategories(StatesGroup):
    choose = State()