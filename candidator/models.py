from django.db import models
from popolo.models import Person, Link
from autoslug import AutoSlugField
from django.utils.encoding import python_2_unicode_compatible
try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation


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
        return u'<%s>' % (self.label)


@python_2_unicode_compatible
class Position(models.Model):
    label = models.CharField(max_length=512)
    topic = models.ForeignKey(Topic, related_name="positions")
    description = models.TextField(blank=True)

    def __str__(self):
        return u'<%s> to <%s>' % (self.label, self.topic.label)


@python_2_unicode_compatible
class TakenPosition(models.Model):
    topic = models.ForeignKey(Topic, related_name="taken_positions")
    position = models.ForeignKey(Position, related_name="taken_positions", null=True, blank=True)
    person = models.ForeignKey(Person, related_name="taken_positions")
    description = models.TextField(blank=True)
    sources = GenericRelation(Link, help_text="Sources of information")

    def __str__(self):
        template_str = u'<%s> says <%s> to <%s>'
        topic = self.topic.label
        if self.position is None:
            template_str = u"<%s> doesn't have an opinion in <%s>"
            return template_str % (self.person, topic)
        label = self.position.label
        try:
            return template_str % (self.person, label, topic)
        except Person.DoesNotExist:
            return template_str % ('Unknown', self.position.label, self.topic.label)


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=1024)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return u'<%s>' % (self.name)
