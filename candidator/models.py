from django.db import models

# Create your models here.

class Topic(models.Model):
    label = models.CharField(max_length=512)
    description = models.TextField()


class Position(models.Model):
    label = models.CharField(max_length=512)
    topic = models.ForeignKey(Topic)
    description = models.TextField()
