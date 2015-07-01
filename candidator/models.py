from django.db import models
from popolo.models import Person
from autoslug import AutoSlugField
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Topic(models.Model):
    label = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', related_name="topics", null=True)
    slug = AutoSlugField(populate_from='label')

    def get_taken_position_for(self, person):
        try:
            return TakenPosition.objects.get(topic=self, person=person)
        except TakenPosition.DoesNotExist:
            return None

    def __str__(self):
        return '<%s>' % (self.label)


@python_2_unicode_compatible
class Position(models.Model):
    label = models.CharField(max_length=512)
    topic = models.ForeignKey(Topic, related_name="positions")
    description = models.TextField(blank=True)

    def __str__(self):
        return '<%s> to <%s>' % (self.label, self.topic.label)


@python_2_unicode_compatible
class TakenPosition(models.Model):
    topic = models.ForeignKey(Topic, related_name="taken_positions")
    position = models.ForeignKey(Position, related_name="taken_positions")
    person = models.ForeignKey(Person, related_name="taken_positions")

    def __str__(self):
        try:
            return '<%s> says <%s> to <%s>' % (self.person, self.position.label, self.topic.label)
        except Person.DoesNotExist:
            return '%s says <%s> to <%s>' % ('Unknown', self.position.label, self.topic.label)


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=1024)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return '<%s>' % (self.name)
