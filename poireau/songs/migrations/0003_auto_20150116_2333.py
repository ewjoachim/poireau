# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0002_part_index_in_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now(tz=utc), verbose_name='Creation date', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime.now(tz=utc), verbose_name='Last modification date', auto_now=True),
            preserve_default=False,
        ),
    ]
