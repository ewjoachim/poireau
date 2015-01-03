# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Singer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("Member"))
    main_section = models.ForeignKey("singers.Section", verbose_name=_("Main Section"))
    roles = models.ManyToManyField("songs.Part", related_name='singers', verbose_name=_("Roles"))

    def __unicode__(self):
        return self.user.username

    class Meta(object):
        app_label = "singers"
        verbose_name = _("Singer")
        verbose_name_plural = _("Singers")


class Section(models.Model):
    name = models.CharField(max_length=64, verbose_name=_("Name"), unique=True)

    def __unicode__(self):
        return self.name

    class Meta(object):
        app_label = "singers"
        verbose_name = _("Section")
        verbose_name_plural = _("Sections")
