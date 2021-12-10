from django.db import models
from PFE.models import User

# Create your models here.
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
