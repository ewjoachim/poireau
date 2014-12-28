# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('singers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section', models.ForeignKey(related_name='parts', verbose_name='Pupitre', blank=True, to='singers.Section', null=True)),
            ],
            options={
                'verbose_name': 'Voix',
                'verbose_name_plural': 'Voix',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.FilePathField(recursive=True, allow_files=False, allow_folders=True, path=b'/Users/mario/code/negitachi/Chansons Negitachi', verbose_name='Chemin')),
                ('name', models.CharField(max_length=512, verbose_name='Nom')),
                ('deleted', models.BooleanField(default=False, verbose_name='Supprim\xe9')),
            ],
            options={
                'verbose_name': 'Chanson',
                'verbose_name_plural': 'Chansons',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='part',
            name='song',
            field=models.ForeignKey(related_name='parts', verbose_name='Chanson', to='songs.Song'),
            preserve_default=True,
        ),
    ]
