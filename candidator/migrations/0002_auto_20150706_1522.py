# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takenposition',
            name='position',
            field=models.ForeignKey(related_name='taken_positions', to='candidator.Position', null=True, on_delete=models.CASCADE),
        ),
    ]
