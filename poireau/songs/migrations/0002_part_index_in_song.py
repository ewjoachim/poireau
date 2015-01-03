# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='index_in_song',
            field=models.IntegerField(help_text='Number of the part in all the unnamed voices in the part (used for unnamed parts only)', null=True, verbose_name='Index', blank=True),
            preserve_default=True,
        ),
    ]
