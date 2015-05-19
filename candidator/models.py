from django.db import models
from popolo.models import Person
from autoslug import AutoSlugField
from django.utils.encoding import force_bytes


class Topic(models.Model):
    label = models.CharField(max_length=512)
    description = models.TextField()
    category = models.ForeignKey('Category', related_name="topics", null=True)
    slug = AutoSlugField(populate_from='label')

    def __str__(self):
        return force_bytes('<%s>' % (self.label))

class Position(models.Model):
    label = models.CharField(max_length=512)
    topic = models.ForeignKey(Topic)
    description = models.TextField()

    def __str__(self):
        return force_bytes('<%s> to <%s>' % (self.label, self.topic.label))


class TakenPosition(models.Model):
    topic = models.ForeignKey(Topic)
    position = models.ForeignKey(Position)
    person = models.ForeignKey(Person)

    def __str__(self):
        return force_bytes('<%s> says <%s> to <%s>' % (self.person, self.position.label, self.topic.label))


class Category(models.Model):
    name = models.CharField(max_length=1024)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return force_bytes('<%s>' % (self.name))

