# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('singers', '0002_auto_20150103_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singer',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='singers', to='songs.Part', verbose_name='Roles'),
        ),
    ]
