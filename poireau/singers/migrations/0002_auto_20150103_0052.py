# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('songs', '0001_initial'),
        ('singers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='singer',
            name='roles',
            field=models.ManyToManyField(related_name='singers', verbose_name='Roles', to='songs.Part'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='singer',
            name='user',
            field=models.OneToOneField(verbose_name='Member', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
