# -*- coding: utf-8 -*-

import os
from io import BytesIO
# import tempfile
# import shutil

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy as reverse

import sh

from ..utils.xml_song import XmlSong


class Song(XmlSong, models.Model):
    xml_content = models.TextField()
    path = models.CharField(max_length=255, verbose_name=_("Path"), help_text=_("Path to the xml file"))

    name = models.CharField(verbose_name=_("Name"), max_length=512)

    date_created = models.DateTimeField(verbose_name=_('Creation date'), auto_now_add=True, blank=True)
    date_modified = models.DateTimeField(verbose_name=_('Last modification date'), auto_now=True, blank=True)

    class Meta(object):
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")

    id_filename = ".id"

    def get_file_content(self):
        return self.xml_content.encode("utf-8")

    def get_absolute_url(self):
        return reverse("songs:song_detail", kwargs={"pk": self.id})

    @property
    def folder(self):
        return os.path.dirname(self.path)

    def create_parts(self):
        for part in self.xml_parts:
            model_part = part.to_model_part()
            self.parts.add(model_part)

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
