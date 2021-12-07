from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=200)
    lastname = models.CharField('last_name',max_length=200)
    firstname = models.CharField('first_name',max_length=200)
    password=models.CharField('password',max_length=200)
    # campus=models.ForeignKey('campus_id')
    moderator=models.BooleanField('moderator',max_length=200)


