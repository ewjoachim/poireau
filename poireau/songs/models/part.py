# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import itertools

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text


class Part(models.Model):
    name = models.CharField(max_length=64)
    song = models.ForeignKey("songs.Song", related_name='parts', verbose_name=_("Song"))
    section = models.ForeignKey("singers.Section", related_name='parts', verbose_name=_("Section"), blank=True, null=True)
    index_in_song = models.IntegerField(
        verbose_name=_("Index"), help_text=_(
            "Number of the part in all the unnamed voices in the part "
            "(used for unnamed parts only)"
        ),
        blank=True, null=True
    )

    def __unicode__(self):
        return self.name

    class Meta(object):
        app_label = "songs"
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        unique_together = [("name", "song")]

    # XML Management Methods

    @classmethod
    def part_from_xml(cls, xml_score_part, xml_tree, song, counter):
        """
        Creates a Part object from the xml content.
            xml_score_part: the ElementTree object referencing the <score-part> tag
            xml_tree: the whole xml tree (used to find the part itself)
            song is the instance of the song to create the part in
            counter is an intertool counter used to give an incremental number to unnamed parts
        """
        part = cls()
        part.set_xml(xml_score_part, xml_tree)
        part.name = part.get_xml_part_name(xml_score_part)
        part.song = song
        if part.name == "":
            part.index_in_song = next(counter)
            part.name = _("Part {number}").format(number=part.index_in_song)

        return part

    @classmethod
    def parts_from_xml(cls, xml_tree, song):
        """
        Create all the part objects from the whole song XML. Returns a list.
        """
        counter = itertools.count(1)  # Indices are 1-based
        return [
            cls.part_from_xml(score_part, xml_tree, song, counter)
            for score_part in xml_tree.getroot().findall("part-list/score-part")
        ]

    def load_xml(self, xml_tree):
        """
        Given an instance of part and the song XML tree, loads the XML part in the
        instance to allow part manipulations
        """
        if self.index_in_song is not None:
            # Retreive by index
            try:
                xml_score_part = [
                    score_part
                    for score_part in xml_tree.getroot().findall("part-list/score-part")
                    if not self.get_xml_part_name(score_part)
                ][self.index_in_song - 1]  # Indices are 1-based
            except IndexError:
                raise ValueError("Part number {} not found in the Song.".format(self.index_in_song))
        else:
            # Retrieve by name
            xml_score_part = next(iter(
                score_part
                for score_part in xml_tree.getroot().findall("part-list/score-part")
                if self.get_xml_part_name(score_part) == self.name
            ), None)
        if xml_score_part is None:
            raise ValueError("Part {} not found in the Song.".format(self.name))

        self.set_xml(xml_score_part, xml_tree)

    def set_xml(self, xml_score_part, xml_tree):
        """
        stores the xml score-part, and from it, find the xml part.
        """
        self.xml_score_part = xml_score_part
        self.xml_part = self.get_xml_part(xml_tree)

    @staticmethod
    def get_xml_part_name(xml_score_part):
        """
        Extracts the name of part from the xml elements
        """
        part_name_node = xml_score_part.find("part-name")
        if part_name_node is not None:
            if part_name_node.get("print-object", "") == "no":
                return ""
        return part_name_node.text if part_name_node is not None else ""

    def get_internal_name(self):
        """
        Extracts the internal name (usually P1, P2 etc) from the
        stored score-part object
        """
        return self.xml_score_part.get("id")

    def get_xml_part(self, xml_tree):
        """
        Find the xml part in the whole song tree
        """
        return next(iter(
            element
            for element in xml_tree.findall("part")
            if element.attrib.get("id") == self.get_internal_name()
        ), None)

    @property
    def first_note(self):
        """
        Returns the first notes of a part
        """
        for xml_note in self.xml_part.iterfind("measure/note"):
            if xml_note.find("rest") is not None:
                continue

            step = xml_note.find("pitch/step").text
            octave = xml_note.find("pitch/octave").text
            alter_node = xml_note.find("pitch/alter")
            alter = alter_node.text if alter_node is not None else ""
            return (
                force_text({
                    "A": _("A"), "B": _("B"), "C": _("C"), "D": _("D"),
                    "E": _("E"), "F": _("F"), "G": _("G")
                }[step]),
                {"1": "♯", "-1": "♭"}.get(alter, ""),
                octave
            )

    def remove_from_xml(self, xml_tree):
        """
        Remove the part from the whole song tree
        """
        xml_tree.getroot().find("part-list").remove(self.xml_score_part)
        xml_tree.getroot().remove(self.xml_part)
