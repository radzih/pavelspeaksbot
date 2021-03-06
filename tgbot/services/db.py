import os
import random
import django
from asgiref.sync import sync_to_async

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'admin_panel.admin_panel.settings'
)
django.setup()

from admin_panel.database.models import Question,\
    User, Level, Word, Word_Category, Tip, Film, \
        FilmCategory

@sync_to_async 
def db_get_questions() -> list:
    questions = Question.objects.filter().order_by('id')
    return list(questions)

@sync_to_async
def db_get_users_telegram_ids() -> list:
    return list(User.objects.all().values('telegram_id'))

@sync_to_async
def db_add_user(telegram_id: int) -> None:
    User(
        telegram_id=telegram_id
    ).save()

@sync_to_async
def db_add_user_level(
    user_level: str,
    telegram_id: int) -> None:
    levels = Level.objects.all()
    for level in levels:
        if level.level == user_level:
            user = User.objects.get(
               telegram_id=telegram_id 
            )
            user.level=level
            user.save()

@sync_to_async
def db_add_user_word_category(
    telegram_id: int,
    category_id: int) -> None:
    category = Word_Category.objects.get(
        id=category_id
    )
    user = User.objects.get(
        telegram_id=telegram_id
    )
    user.words_categories.add(category)
    user.save()

@sync_to_async
def db_add_user_film_category(
    telegram_id: int,
    category_id: int) -> None:
    category = FilmCategory.objects.get(
        id=category_id
    )
    user = User.objects.get(
        telegram_id=telegram_id
    )
    user.films_categories.add(category)
    user.save()


@sync_to_async
def db_remove_user_word_category(
    telegram_id: int,
    category_id: int) -> None:
    category = Word_Category.objects.get(
        id=category_id
    )
    user = User.objects.get(
        telegram_id=telegram_id
    )
    user.words_categories.remove(
        category
    )


@sync_to_async
def db_remove_user_film_category(
    telegram_id: int,
    category_id: int) -> None:
    category = FilmCategory.objects.get(
        id=category_id
    )
    user = User.objects.get(
        telegram_id=telegram_id
    )
    user.films_categories.remove(
        category
    )

@sync_to_async
def db_get_user_categories(
    telegram_id: int,
    category: str) -> list:
    user = User.objects.get(
        telegram_id=telegram_id
    )
    categories = {
        'word': user.words_categories,
        'film': user.films_categories,
    }
    return list(categories.get(category).all()) 

@sync_to_async
def db_get_random_word(telegram_id: int) -> Word:
    user = User.objects.get(telegram_id=telegram_id)
    user_words_categories = user.words_categories.all()
    if not user_words_categories:
        words = Word.objects.filter(
            level=user.level
        ).order_by('?')
    else:
        words = Word.objects.filter(
            category__in=user_words_categories,
            level=user.level
        ).order_by('?')
    unique_words  = list(set(words) - set(user.words.all()))
    random.shuffle(unique_words)
    random_word = unique_words[0]
    user.words.add(random_word)
    user.save()
    return random_word

@sync_to_async
def db_get_random_film(telegram_id: int) -> Film:
    user = User.objects.get(telegram_id=telegram_id)
    user_films_categories = user.films_categories.all()
    if not user_films_categories:
        films = Film.objects.filter(
            level=user.level
        ).order_by('?')
    else:
        films = Film.objects.filter(
            category__in=user_films_categories,
            level=user.level
        ).order_by('?')
    unique_films = list(set(films) - set(user.films.all()))
    random.shuffle(unique_films)
    random_film = unique_films[0]
    user.films.add(random_film)
    user.save()
    return random_film

@sync_to_async
def db_get_random_tip(telegram_id: int) -> Tip:
    user = User.objects.get(telegram_id=telegram_id)
    user_tips = user.tips.all()
    random_tip = set(Tip.objects.all().order_by('?')) - set(user_tips) 
    user.tips.add(list(random_tip)[0])
    return list(random_tip)[0]

@sync_to_async
def db_get_user_info(telegram_id: int) -> tuple:
    user = User.objects.get(
        telegram_id=telegram_id
    )
    return user.telegram_id, user.level, \
        list(user.words.all().order_by('?')), list(user.words_categories.all())

@sync_to_async
def db_get_categories(
    level: Level,
    category: str) -> list:
    categories = {
        'word': Word_Category,
        'film': FilmCategory,
    }
    CategoryObject = categories.get(category)
    return list(
        CategoryObject.objects.filter(
            level=level
        ).all()
        )

@sync_to_async
def db_delete_categories(
    telegram_id: int,
    category: str) -> None:
    user = User.objects.get(
        telegram_id=telegram_id
    )
    categories = {
        'word': user.words_categories,
        'film': user.films_categories 
    }
    
    categories.get(category).clear()