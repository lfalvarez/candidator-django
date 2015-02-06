from django.db import models
from popolo.models import Person
from autoslug import AutoSlugField


class Topic(models.Model):
    label = models.CharField(max_length=512)
    description = models.TextField()
    category = models.ForeignKey('Category', related_name="topics", null=True)


class Position(models.Model):
    label = models.CharField(max_length=512)
    topic = models.ForeignKey(Topic)
    description = models.TextField()


class TakenPosition(models.Model):
    topic = models.ForeignKey(Topic)
    position = models.ForeignKey(Position)
    person = models.ForeignKey(Person)


class Category(models.Model):
    name = models.CharField(max_length=1024)
    slug = AutoSlugField(populate_from='name')
