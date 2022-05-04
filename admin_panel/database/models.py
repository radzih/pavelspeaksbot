from django.db import models
from django.forms import JSONField

# Create your models here.


class Question(models.Model):
    question = models.CharField(max_length=255)
    answers = models.JSONField()
    correct_answer = models.CharField(max_length=255)
    point = models.IntegerField()

        

class Level(models.Model):
    level = models.CharField(max_length=255)

class Word_Category(models.Model):
    category = models.CharField(max_length=255)

class Word(models.Model):
    word = models.CharField(max_length=255)
    translate = models.CharField(max_length=255)
    audio_path = models.CharField(max_length=255)
    category = models.ForeignKey(Word_Category, on_delete=models.PROTECT)
    level = models.ForeignKey(Level, on_delete=models.PROTECT)

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    level = models.ForeignKey(Level, on_delete=models.PROTECT, null=True)
    words = models.ManyToManyField(Word, blank=True)
    words_categories = models.ManyToManyField(Word_Category, blank=True)

