# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.


class Singer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Membre")
    main_section = models.ForeignKey("singers.Section", verbose_name="Pupitre principal")
    roles = models.ManyToManyField("songs.Part", related_name='singers', verbose_name='Roles')

    class Meta(object):
        app_label = "singers"
        verbose_name = "Membre chantant"
        verbose_name_plural = "Membres chantant"


class Section(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nom', unique=True)

    def __unicode__(self):
        return self.name

    class Meta(object):
        app_label = "singers"
        verbose_name = "Pupitre"
        verbose_name_plural = "Pupitres"


