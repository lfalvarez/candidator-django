# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidator', '0002_auto_20150706_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='takenposition',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
