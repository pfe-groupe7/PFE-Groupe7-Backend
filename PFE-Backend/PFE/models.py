from django.db import models


class User(models.Model):
    id=models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200,unique=True)
    lastname = models.CharField('last_name',max_length=200)
    firstname = models.CharField('first_name',max_length=200)
    password=models.CharField('password',max_length=200)
    
    moderator=models.BooleanField('moderator',max_length=200)
    campus=models.IntegerField('campus_id',default=1)


