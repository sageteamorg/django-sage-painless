from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Answer(models.Model):
    sku = models.CharField(unique=True, max_length=-1)
    code = models.CharField(max_length=-1, blank=True, null=True)
    content = models.CharField(max_length=-1)
    question = models.ForeignKey('Question', models.DO_NOTHING, db_column='question', blank=True, null=True)
    responder = models.ForeignKey('User', models.DO_NOTHING, db_column='responder', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Answer'


class Question(models.Model):
    sku = models.CharField(unique=True, max_length=-1)
    text = models.CharField(max_length=-1)
    code = models.CharField(max_length=-1, blank=True, null=True)
    content = models.CharField(max_length=-1)
    topic = models.ForeignKey('Topic', models.DO_NOTHING, db_column='topic', blank=True, null=True)
    asker = models.ForeignKey('User', models.DO_NOTHING, db_column='asker', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Question'


class Topic(models.Model):
    sku = models.CharField(unique=True, max_length=-1)
    title = models.CharField(max_length=-1)
    content = models.CharField(max_length=-1)
    creator = models.ForeignKey('User', models.DO_NOTHING, db_column='creator', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Topic'


class User(models.Model):
    username = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class Vote(models.Model):
    sku = models.CharField(unique=True, max_length=-1)
    object_id = models.CharField(max_length=-1)
    scope = models.TextField(blank=True, null=True)  # This field type is a guess.
    kind = models.TextField(blank=True, null=True)  # This field type is a guess.
    candidate = models.ForeignKey(User, models.DO_NOTHING, db_column='candidate', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Vote'
