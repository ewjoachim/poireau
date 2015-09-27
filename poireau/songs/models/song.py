# -*- coding: utf-8 -*-

import os
from io import BytesIO
# import tempfile
# import shutil

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy as reverse
from django.utils.functional import cached_property
from django.apps import apps

import sh

from ..utils.xml_song import DBSong


class Song(models.Model):
    xml_content = models.TextField()
    path = models.CharField(max_length=255, verbose_name=_("Path"), help_text=_("Path to the xml file"), unique=True)

    name = models.CharField(verbose_name=_("Name"), max_length=512, unique=True)

    date_created = models.DateTimeField(verbose_name=_('Creation date'), auto_now_add=True, blank=True)
    date_modified = models.DateTimeField(verbose_name=_('Last modification date'), auto_now=True, blank=True)

    class Meta(object):
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")

    @property
    def folder(self):
        return os.path.dirname(self.path)

    @property
    def category(self):
        return os.path.basename(os.path.dirname(self.folder))

    @property
    def sort_key(self):
        return (len(self.path.split(os.sep)), self.category)

    @cached_property
    def xml_song(self):
        return DBSong(
            model_instance=self
        )

    def get_absolute_url(self):
        return reverse("songs:song_detail", kwargs={"pk": self.id})

    def create_model_parts(self):
        """
        Returns new instances of model parts (not saved yet)
        by reading the xml content and extracting the parts.
        """
        if not self.id:
            raise ValueError("Cannot create parts if Song has not been saved yet.")
        xml_parts = list(self.xml_song.xml_parts)
        names = {part.name for part in xml_parts}
        Section = apps.get_model("singers", "Section")
        sections = dict(Section.objects.filter(name__in=names).values_list("name", "id"))
        model_parts = []
        for xml_part in xml_parts:
            model_part = xml_part.to_model_part()
            model_part.song_id = self.id
            model_part.id = sections.get(model_part.name)
            model_parts.append(model_part)
        return model_parts

    def __str__(self):
        return self.name

    def export(self):
        """
        Will export the current state of the xml file to pdf (score) and midi.
        This method is still in debug state.
        """
        output = BytesIO()
        self.parsed_xml.write(output)

        # dir_path = tempfile.mkdtemp()
        dir_path = "."
        try:
            old_dir = os.getcwd()
            os.chdir(dir_path)

            lily_content = sh.musicxml2ly("--nd", "--nrp", "--npl", "--no-beaming", "-l", "french", "-m", "-", "-o", "-", _in=output.getvalue())

            sh.lilypond("-o", os.path.join(dir_path, "output"), "-", _in=str(lily_content))

            # For now, we leave it as is, after creating a pdf file and a midi file.
            # Midi to mp3 conversion can be done :
            # http://devonbryant.github.io/blog/2013/08/24/midi-to-audio-conversion-with-python/

        finally:
            os.chdir(old_dir)
            # shutil.rmtree(dir_path)
