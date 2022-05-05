from aiogram.dispatcher.filters.state \
    import StatesGroup, State

class ChooseCategories(StatesGroup):
    words_categories = State()