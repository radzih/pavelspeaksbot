from email.mime import audio
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
    Level, Word, Word_Category, Tip

def add_test(questions: list) -> None:
    for question in questions:
        if len(question.get('answers')) > 2:
            answers = question.get('answers') + ['He знаю']
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
        word_level_object = Level.objects.get(
            level=word.get('level')
        ) 

        try:
            word_category_object = Word_Category.objects.get(
                category=word.get('category'),
                level=word_level_object
            )
        except:
            word_category_object = Word_Category(
                category=word.get('category'),
                level=word_level_object
            )
            word_category_object.save()
           
        Word(
            word=word.get('word'),
            translate=word.get('translate'),
            category=word_category_object,
            level=word_level_object,
            audio_path=f'/data/audio/files/{word.get("uuid")}.mp3'
        ).save()

def add_tips() -> None:
    PATH_TO_TIPS = 'data/audio/tips/'
    tips_filenames = os.listdir(PATH_TO_TIPS)
    for filename in tips_filenames:
        Tip(
            audio_path= PATH_TO_TIPS + filename
        ).save()
    

add_test(questions)
add_levels()
add_words_and_words_categories(words)
add_tips()