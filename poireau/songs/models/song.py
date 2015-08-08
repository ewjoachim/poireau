# -*- coding: utf-8 -*-

import os
from io import BytesIO
from xml.etree import ElementTree as ET
# import tempfile
# import shutil

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse_lazy as reverse

import sh


class Song(models.Model):
    path = models.FilePathField(
        verbose_name=_("Path"), path=settings.SONGS_FOLDER, recursive=True,
        allow_folders=True, allow_files=False, blank=True
    )
    name = models.CharField(verbose_name=_("Name"), max_length=512)

    date_created = models.DateTimeField(verbose_name=_('Creation date'), auto_now_add=True, blank=True)
    date_modified = models.DateTimeField(verbose_name=_('Last modification date'), auto_now=True, blank=True)

    class Meta(object):
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")

    id_filename = ".id"

    def get_absolute_url(self):
        return reverse("songs:song_detail", kwargs={"pk": self.id})

    @property
    def folder(self):
        return os.path.basename(os.path.dirname(self.path))

    @property
    def xml(self):
        try:
            list_dir = [
                filename
                for filename in os.listdir(self.path)
            ]
            xml = next(filename for filename in sorted(list_dir) if filename.endswith(".xml"))
            return os.path.join(self.path, xml)
        except StopIteration:
            raise ValueError("XML file not found !")
        except FileNotFoundError:
            raise ValueError("Can't open folder !")

    def __str__(self):
        return self.name

    def create_id_file(self):
        if self.id is None:
            raise ValueError("Cannot create id file when id is not set !")
        with open(os.path.join(self.path, self.id_filename), "w") as id_file:
            id_file.write("{}".format(self.id))

    def create_parts(self):
        Part = models.get_model("songs", "Part")
        parts = Part.parts_from_xml(xml_tree=self.parsed_xml, song=self)
        sections = {section.name: section for section in models.get_model("singers", "Section").objects.all()}
        for part in parts:
            part.section = sections.get(part.name, None)

        Part.objects.bulk_create(parts)
        return parts

    @classmethod
    def song_from_path(cls, path, name_xml, song_id=None):
        # name_xml = name_xml[:-4]
        name_dir = os.path.basename(path)
        name = name_dir  # if name_dir == name_xml else "{} ({})".format(name_dir, name_xml)
        return cls(name=name, path=path, id=song_id)

    @classmethod
    def explore_folder(cls, base_path, songs_in_db):
        new_songs, existing_songs = [], []

        song_by_id = {song.id: song for song in songs_in_db}

        for path, __, files in os.walk(base_path):
            path = os.path.join(os.path.dirname(os.path.abspath(base_path)), path)
            try:
                xml = next(filename for filename in files if filename.endswith(".xml"))
            except StopIteration:
                continue

            if cls.id_filename in files:
                try:
                    with open(os.path.join(path, cls.id_filename), "r") as id_file:
                        song_id = int(next(id_file).strip())
                except ValueError:
                    raise ValueError("Malformed .id file in {}".format(path))
                try:
                    song = song_by_id[song_id]
                    if path != song.path:
                        song.path = path
                        song.moved = True
                    existing_songs.append(song)
                except KeyError:
                    new_songs.append(cls.song_from_path(
                        path=path,
                        name_xml=xml,
                        song_id=song_id
                    ))
            else:
                new_songs.append(cls.song_from_path(
                    path=path,
                    name_xml=xml,
                ))

        return new_songs, existing_songs

    @classmethod
    def discover_songs_changes(cls, path=None, commit=True):
        """
        Looks in the dropbox folder and synchronises the songs and their names/paths.
        """
        path = path or settings.SONGS_FOLDER

        songs_in_db = list(cls.objects.exclude(path=""))

        new_songs, existing_songs = cls.explore_folder(path, songs_in_db)

        existing_ids = set(element.id for element in existing_songs)

        moved_songs = [song for song in existing_songs if getattr(song, "moved", False)]

        deleted_songs = [song for song in songs_in_db if song.id not in existing_ids]

        if commit:
            for song in deleted_songs:
                song.path = ""
                song.full_clean()
                song.save()
            for song in new_songs:
                song.full_clean()
                song.save()
                song.create_id_file()
                song.create_parts()
            for song in moved_songs:
                song.full_clean()
                song.save()

        return {"new": new_songs, "deleted": deleted_songs, "moved": moved_songs}

    @property
    def parsed_xml(self):
        if not hasattr(self, "_parsed_xml"):
            with open(self.xml) as file_handler:
                self._parsed_xml = ET.parse(file_handler)
        return self._parsed_xml

    @cached_property
    def xml_parts(self):
        parts = list(self.parts.all())
        try:
            for part in parts:
                part.load_xml(self.parsed_xml)
        except ValueError:
            return []

        return parts

    def keep_one_part(self, keep_part):
        for part in self.xml_parts:
            if part is not keep_part:
                part.remove_from_xml(self.parsed_xml)

    def remove_xml_part(self, part):
        part.remove_from_xml(self.parsed_xml)

    def first_notes(self):
        return {part: part.first_note for part in self.xml_parts}

    def display_first_notes(self):
        display_notes = []
        first_notes = self.first_notes()

        for part in self.parts.all():
            note = first_notes[part]
            display_notes.append("{part} : {note}".format(
                part=part.name,
                note=note,
            ))
        return display_notes

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

