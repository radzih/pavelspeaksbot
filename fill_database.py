import os
import json
import django

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'admin_panel.admin_panel.settings'
)
django.setup()

from data.test.test import questions
from admin_panel.database.models import Question, \
    Level

def add_test(questions: list) -> None:
    for question in questions:
        if len(question.get('answers')) > 2:
            answers = question.get('answers') + ['He znayu']
        else:
            answers = question.get('answers')
        Question(
            question=question.get('question'),
            correct_answer=question.get('answers')[
                question.get('correct_index')
            ],
            answers=json.dumps(answers),
            point=question.get('point'),
        ).save()

def add_levels() -> None:
    Level(
        level='Низкий'
    ).save()
    Level(
        level='Средний'
    ).save()


add_test(questions)
add_levels()