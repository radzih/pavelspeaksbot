import os
import django
from asgiref.sync import sync_to_async

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'admin_panel.admin_panel.settings'
)
django.setup()

from admin_panel.database.models import Question,\
    User, Level, Word

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
def db_get_random_word(telegram_id: int) -> Word:
    user = User.objects.get(telegram_id=telegram_id)
    user_words_categories = user.words_categories.all()
    if not user_words_categories:
        random_word = Word.objects.filter(
            level=user.level
        ).order_by('?').first()
    else:
        random_word = Word.objects.filter(
            category__in=user_words_categories,
            level=user.level
        ).order_by('?').first()
    user.words.add(random_word)
    user.save()
    return random_word