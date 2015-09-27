# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_auto_20150116_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='path',
        ),
        migrations.AddField(
            model_name='song',
            name='xml_content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
