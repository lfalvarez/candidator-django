from django.db import models
from popolo.models import Person

# Create your models here.

class Topic(models.Model):
    label = models.CharField(max_length=512)
    description = models.TextField()

class Position(models.Model):
    label = models.CharField(max_length=512)
    topic = models.ForeignKey(Topic)
    description = models.TextField()

class TakenPosition(models.Model):
    topic = models.ForeignKey(Topic)
    position = models.ForeignKey(Position)
    person = models.ForeignKey(Person)
