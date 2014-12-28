# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0004_auto_20141227_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='path',
            field=models.FilePathField(recursive=True, allow_files=False, allow_folders=True, blank=True, path='/Users/mario/code/negitachi/Chansons Negitachi', verbose_name='Chemin'),
            preserve_default=True,
        ),
    ]
