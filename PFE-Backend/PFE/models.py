from enum import unique

from django.db import models
from django.db.models.base import Model, ModelState
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import CASCADE

class Campus(models.Model):
    id = models.AutoField('campus_id',primary_key=True)
    campusName = models.CharField('campus_name',unique=True,max_length=64)


class Location(models.Model):
    id = models.AutoField('location_id',primary_key=True)
    name = models.CharField('name',max_length=256)
    address = models.CharField('address',max_length=512)
    campus = models.ForeignKey('campus',on_delete=CASCADE,default=1)


class User(models.Model):
    id = models.AutoField("user_id",primary_key=True)
    email = models.EmailField(max_length=200, unique=True)
    lastname = models.CharField('last_name', max_length=200)
    firstname = models.CharField('first_name', max_length=200)
    password = models.CharField('password', max_length=200)
    moderator = models.BooleanField('is_moderator', max_length=200, default=False)
    campus = models.ForeignKey('campus',on_delete=models.CASCADE,default=1)

class AdsCampus(models.Model):
    ad = models.ForeignKey('ad',on_delete=models.CASCADE,default=1)
    campus= models.ForeignKey('campus',on_delete=models.CASCADE,default=1)
    UniqueConstraint(fields = ['ad', 'campus'], name = 'composite id')

class Media(models.Model):
    id = models.AutoField('media_id',primary_key=True)
    url = models.CharField('url',max_length=2048)
    ad = models.ForeignKey('ad',on_delete=models.CASCADE,default=1)

class Category(models.Model):
    id = models.AutoField('category_id',primary_key=True)
    categoryName = models.CharField('category_name',max_length=64,unique=True)
    parent = models.ForeignKey('category',on_delete=models.CASCADE,blank=True,null=True)

class Ad(models.Model):
    class Status(models.TextChoices):
        TOSELL = 'à vendre'
        TOGIVE = 'à donner'

    class State(models.TextChoices):
        PUBLISHED = 'publié'
        PENDING = 'attendre validation'
        REJECTED = 'refusé'
        CLOSED = 'clôturé'

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=64, choices=Status.choices)
    title = models.CharField('title', max_length=200)
    description = models.CharField('description', max_length=2048)
    state = models.CharField(
        max_length=64, choices=State.choices, default=State.PENDING)
    price = models.IntegerField('price')
    seller = models.ForeignKey('user',on_delete=models.CASCADE,default=1)






