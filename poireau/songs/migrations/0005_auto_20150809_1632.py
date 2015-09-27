# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0004_auto_20150809_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='index_in_song',
        ),
        migrations.AddField(
            model_name='part',
            name='first_note_accidental',
            field=models.CharField(blank=True, choices=[('flat', '♭'), ('natural', ''), ('sharp', '♯')], max_length=1, verbose_name='First note accidental', default='natural'),
        ),
        migrations.AddField(
            model_name='part',
            name='first_note_midi',
            field=models.IntegerField(blank=True, null=True, verbose_name='First note'),
        ),
    ]
