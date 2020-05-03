# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidator', '0003_takenposition_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takenposition',
            name='position',
            field=models.ForeignKey(related_name='taken_positions', blank=True, to='candidator.Position', null=True, on_delete=models.CASCADE),
        ),
    ]
