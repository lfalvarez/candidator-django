# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('popolo', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TakenPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.ForeignKey(related_name='taken_positions', to='popolo.Person', on_delete=models.CASCADE)),
                ('position', models.ForeignKey(related_name='taken_positions', to='candidator.Position', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=512)),
                ('description', models.TextField(blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('category', models.ForeignKey(related_name='topics', to='candidator.Category', null=True, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='takenposition',
            name='topic',
            field=models.ForeignKey(related_name='taken_positions', to='candidator.Topic', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='position',
            name='topic',
            field=models.ForeignKey(related_name='positions', to='candidator.Topic', on_delete=models.CASCADE),
        ),
    ]
