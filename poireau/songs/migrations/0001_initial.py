# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('singers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('section', models.ForeignKey(related_name='parts', verbose_name='Section', blank=True, to='singers.Section', null=True)),
            ],
            options={
                'verbose_name': 'Part',
                'verbose_name_plural': 'Parts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.FilePathField(recursive=True, allow_files=False, allow_folders=True, blank=True, path=settings.SONGS_FOLDER, verbose_name='Path')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Song',
                'verbose_name_plural': 'Songs',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='part',
            name='song',
            field=models.ForeignKey(related_name='parts', verbose_name='Song', to='songs.Song'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='part',
            unique_together=set([('name', 'song')]),
        ),
    ]
