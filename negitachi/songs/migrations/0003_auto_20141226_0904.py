# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0002_auto_20141225_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='deleted',
        ),
        migrations.AddField(
            model_name='song',
            name='not_found',
            field=models.BooleanField(default=False, verbose_name='Introuvable'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='part',
            name='name',
            field=models.CharField(unique=True, max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(unique=True, max_length=512, verbose_name='Nom'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='path',
            field=models.FilePathField(recursive=True, allow_files=False, allow_folders=True, path='/Users/mario/code/negitachi/Chansons Negitachi', unique=True, verbose_name='Chemin'),
            preserve_default=True,
        ),
    ]
