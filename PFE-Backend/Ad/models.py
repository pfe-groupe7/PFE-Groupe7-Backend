from django.db import models

# Create your models here.
# Enums for Ad
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
    seller_id = models.IntegerField('user_id', default=1)

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.title