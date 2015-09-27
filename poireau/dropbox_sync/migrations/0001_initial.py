# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FolderSync',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('cursor', models.CharField(null=True, max_length=512, verbose_name='cursor')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
                ('dropbox_path', models.CharField(max_length=512, verbose_name='dropbox path')),
                ('local_path', models.CharField(max_length=512, verbose_name='local path')),
            ],
            options={
                'verbose_name_plural': 'Folder Syncs',
                'verbose_name': 'Folder Sync',
            },
        ),
    ]
