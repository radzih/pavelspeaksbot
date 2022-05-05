import os
import json
import django

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'admin_panel.admin_panel.settings'
)
django.setup()

from data.test.test import questions
from data.words.words import words
from admin_panel.database.models import Question, \
    Level, Word, Word_Category

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

def add_words_and_words_categories(words: list) -> None:
    for word in words:
        added_words_categories = [
            cat.category for cat in Word_Category.objects.all()
        ]
        word_level_object = Level.objects.get(
            level=word.get('level')
        ) 

        if word.get('category') not in added_words_categories:
            Word_Category(
                category=word.get('category'),
                level=word_level_object
            ).save()
        word_category_object = Word_Category.objects.get(
            category=word.get('category'),
            level=word_level_object
        )
           
        Word(
            word=word.get('word'),
            translate=word.get('translate'),
            category=word_category_object,
            level=word_level_object,
            audio_path=f'/data/audio/files/{word.get("uuid")}.mp3'
        ).save()

add_test(questions)
add_levels()
add_words_and_words_categories(words)