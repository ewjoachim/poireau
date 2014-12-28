# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='Nom')),
            ],
            options={
                'verbose_name': 'Pupitre',
                'verbose_name_plural': 'Pupitres',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('main_section', models.ForeignKey(verbose_name='Pupitre principal', to='singers.Section')),
            ],
            options={
                'verbose_name': 'Membre chantant',
                'verbose_name_plural': 'Membres chantant',
            },
            bases=(models.Model,),
        ),
    ]
