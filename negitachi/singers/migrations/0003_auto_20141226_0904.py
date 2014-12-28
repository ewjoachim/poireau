# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('singers', '0002_auto_20141224_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(unique=True, max_length=64, verbose_name='Nom'),
            preserve_default=True,
        ),
    ]
