# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_auto_20141226_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='not_found',
        ),
        migrations.AlterField(
            model_name='song',
            name='path',
            field=models.FilePathField(recursive=True, allow_files=False, allow_folders=True, blank=True, path='/Users/mario/code/negitachi/negitachi/Chansons Negitachi', unique=True, verbose_name='Chemin'),
            preserve_default=True,
        ),
    ]
