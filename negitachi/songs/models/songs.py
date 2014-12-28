# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from cStringIO import StringIO
from xml.etree import ElementTree as ET

from django.db import models
from django.conf import settings

import sh


class Song(models.Model):
    path = models.FilePathField(
        verbose_name="Chemin", path=settings.SONGS_FOLDER, recursive=True,
        allow_folders=True, allow_files=False, blank=True
    )
    name = models.CharField(verbose_name="Nom", max_length=512)

    class Meta(object):
        verbose_name = "Chanson"
        verbose_name_plural = "Chansons"

    id_filename = ".id"

    @property
    def xml(self):
        try:
            xml = next(filename for filename in sorted(os.listdir(self.path)) if filename.endswith(".xml"))
            return os.path.join(self.path, xml)
        except StopIteration:
            raise ValueError("XML file not found !")

    def __unicode__(self):
        return self.name

    def create_id_file(self):
        if self.id is None:
            raise ValueError("Cannot create id file when id is not set !")
        with open(os.path.join(self.path, self.id_filename), "w") as id_file:
            id_file.write("{}".format(self.id))

    @classmethod
    def explore_folder(cls, songs_in_db):
        new_songs, existing_songs = [], []

        song_by_id = {song.id: song for song in songs_in_db}

        for path, __, files in os.walk(settings.SONGS_FOLDER):
            path = path
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
                except KeyError:
                    raise ValueError(".id contains non-existant id in {}".format(path))
                if path != song.path:
                    song.path = path
                    song.moved = True
                existing_songs.append(song)
            else:
                name_xml = xml[:-4]
                name_dir = os.path.basename(path)
                name = name_dir if name_dir == name_xml else "{} ({})".format(name_dir, name_xml)
                song = cls(name=name, path=path)

                new_songs.append(song)

        return new_songs, existing_songs

    @classmethod
    def discover_songs_changes(cls, commit=True):
        """
        Looks in the dropbox folder and synchronises the songs and their names/paths.
        """
        songs_in_db = list(cls.objects.exclude(path=""))

        new_songs, existing_songs = cls.explore_folder(songs_in_db)

        existing_ids = set(element.id for element in existing_songs)

        moved_songs = [song for song in existing_songs if getattr(song, "moved", False)]

        deleted_songs = [song for song in songs_in_db if song.id not in existing_ids]

        if commit:
            for song in deleted_songs:
                song.path = ""
                song.clean()
                song.save()
            for song in new_songs:
                song.clean()
                song.save()
                song.create_id_file()
            for song in moved_songs:
                song.save()

        return {"new": new_songs, "deleted": deleted_songs, "moved": moved_songs}

    def parse_xml(self):
        with open(self.xml) as file_handler:
            self.parsed_xml = ET.parse(file_handler)

    def compute_parts(self):
        if hasattr(self, '_parts'):
            if self.parsed_xml is None:
                raise ValueError("XML file not provided")
            self._parts = self.parsed_xml.getroot().findall("part-list/score-part")
            self._part_list = self.parsed_xml.getroot().find("part-list")
            self._parts_by_name = {part.find("part-name").text: part for part in self._parts if part.find("part-name") is not None}

    @property
    def parts(self):
        self.compute_parts()
        return self._parts

    @property
    def parts_by_name(self):
        self.compute_parts()
        return self._parts_by_name

    @property
    def part_list(self):
        self.compute_parts()
        return self._part_list

    def keep_part(self, name):
        ids_to_remove = set()
        for part_name, part in self.parts_by_name.iteritems():
            if part_name != name:
                ids_to_remove.add(part.attrib["id"])
                self.part_list.remove(part)
        for notes_part in self.xml.findall("part"):
            if notes_part.attrib["id"] in ids_to_remove:
                self.xml.getroot().remove(notes_part)

    def remove_part(self, name):
        part = self.parts_by_name[name]
        part_id = part.attrib[id]
        self.part_list.remove(part)
        try:
            notes_part = [notes_part for notes_part in self.xml.findall("part") if notes_part.attrib["id"] == part_id][0]
            self.xml.getroot().remove(notes_part)
        except IndexError:
            pass

    def export(self, filename="output", export_as=None):
        """
        Filename is without extension
        """
        output = StringIO()
        self.xml.write(output)

        lily_content = sh.musicxml2ly("--npl", "-l", "french", "-", "-o", "-", _in=output.getvalue())

        if "xml" in export_as:
            with open("{}.xml".format(filename), "w") as xml_file:
                xml_file.write(output.getvalue())

        if "ly" in export_as:
            with open("{}.ly".format(filename), "w") as ly_file:
                ly_file.write(str(lily_content))

        sh.lilypond("-o", filename, "-", _in=str(lily_content))
