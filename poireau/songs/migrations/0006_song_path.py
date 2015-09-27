# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0005_auto_20150809_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='path',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
    ]
