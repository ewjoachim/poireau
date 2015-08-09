# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Part(models.Model):

    NOTES = (
        ("a", _("A")),
        ("b", _("B")),
        ("c", _("C")),
        ("d", _("D")),
        ("e", _("E")),
        ("f", _("F")),
        ("g", _("G")),
    )
    ACCIDENTALS = (
        ("flat", _("♭")),
        ("natural", ""),
        ("sharp", _("♯")),
    )
    NOTES_ORDER = "cdefgab"

    name = models.CharField(max_length=64)
    song = models.ForeignKey("songs.Song", related_name='parts', verbose_name=_("Song"))
    section = models.ForeignKey("singers.Section", related_name='parts', verbose_name=_("Section"), blank=True, null=True)
    first_note_midi = models.IntegerField(verbose_name=_("First note"), blank=True, null=True)
    first_note_accidental = models.CharField(max_length=1, choices=ACCIDENTALS, default="natural", verbose_name=_("First note accidental"), blank=True)

    @property
    def first_note(self):
        return Note(self.first_note_midi, self.first_note_accidental)

    @first_note.setter
    def first_note(self, note):
        self.first_note_midi = note.midi_value
        self.first_note_accidental = note.accidental

    def __str__(self):
        return "{} - {}".format(self.song.name, self.name)

    class Meta(object):
        app_label = "songs"
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        unique_together = [("name", "song")]


class Note(object):
    def __init__(self, midi_value, accidental="natural"):
        """
        Midi values : 1 per half tone, C4 == 60
        1 octave == 12 half tones == 12 values. 0 would be "C-1"
        """
        self.midi_value = midi_value
        self.note = Part.NOTES_ORDER[midi_value % 12]
        self.octave = midi_value // 12 - 1
        self.accidental = accidental

    def __str__(self):
        return "{note}{accidental}{octave}".format(
            note=dict(Part.NOTES)[self.note],
            accidental=dict(Part.ACCIDENTALS)[self.accidental],
            octave=_(" (oct. {})").format(self.octave)
        )
