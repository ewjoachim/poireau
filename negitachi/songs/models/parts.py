# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Part(models.Model):
    name = models.CharField(max_length=64, unique=True)
    song = models.ForeignKey("songs.Song", related_name='parts', verbose_name="Chanson")
    section = models.ForeignKey("singers.Section", related_name='parts', verbose_name="Pupitre", blank=True, null=True)

    class Meta(object):
        app_label = "songs"
        verbose_name = "Voix"
        verbose_name_plural = "Voix"
