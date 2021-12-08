from django.db import models
from enum import Enum

from django.db.models.enums import Choices


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200, unique=True)
    lastname = models.CharField('last_name', max_length=200)
    firstname = models.CharField('first_name', max_length=200)
    password = models.CharField('password', max_length=200)

    moderator = models.BooleanField('moderator', max_length=200)
    campus = models.IntegerField('campus_id', default=1)


# Enums for Ad


class Ad(models.Model):
    class Status(models.TextChoices):
        TOSELL = 'to sell'
        TOGIVE = 'to give away'

    class State(models.TextChoices):
        PUBLISHED = 'published'
        PENDING = 'awaiting validation'
        REJECTED = 'rejected'
        CLOSED = 'closed'

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=64, choices=Status.choices)
    title = models.CharField('title', max_length=200)
    description = models.CharField('description', max_length=2048)
    state = models.CharField(
        max_length=64, choices=State.choices, default=State.PENDING)
    price = models.IntegerField('price')
    seller_id = models.ForeignKey('User', User)
