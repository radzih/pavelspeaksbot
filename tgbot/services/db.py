import os
import django
from asgiref.sync import sync_to_async

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'admin_panel.admin_panel.settings'
)
django.setup()

from admin_panel.database.models import Question,\
    User, Level

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



