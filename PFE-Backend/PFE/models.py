from django.db import models
from django.db.models.deletion import CASCADE


class User(models.Model):
    id = models.AutoField("user_id",primary_key=True)
    email = models.EmailField(max_length=200, unique=True)
    lastname = models.CharField('last_name', max_length=200)
    firstname = models.CharField('first_name', max_length=200)
    password = models.CharField('password', max_length=200)

    moderator = models.BooleanField('is_moderator', max_length=200, default=False)
    campus = models.ForeignKey('campus',on_delete=models.CASCADE,default=1)

class Campus(models.Model):
    id = models.AutoField(primary_key=True)
    campusName = models.CharField('campus_name',unique=True,max_length=64)


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name',max_length=256)
    address = models.CharField('address',max_length=512)
    campus = models.ForeignKey('campus',on_delete=CASCADE,default=1)
