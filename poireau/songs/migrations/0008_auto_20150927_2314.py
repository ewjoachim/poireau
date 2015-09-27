# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0007_auto_20150809_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='path',
            field=models.CharField(max_length=255, help_text='Path to the xml file', unique=True, verbose_name='Path'),
        ),
    ]
