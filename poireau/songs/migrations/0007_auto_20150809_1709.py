# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0006_song_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='path',
            field=models.CharField(max_length=255, verbose_name='Path', help_text='Path to the xml file'),
        ),
    ]
