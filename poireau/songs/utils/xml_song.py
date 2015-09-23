import os
import hashlib
import itertools
from io import BytesIO

from lxml import objectify

from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.functional import cached_property
from django.apps import apps


class XmlSong(object):

    def get_file_content(self):
        raise NotImplementedError()

    @property
    def sha1(self):
        return hashlib.sha1(self.file_content).hexdigest()

    @cached_property
    def file_content(self):
        return self.get_file_content()

    def as_bytes_file(self):
        return BytesIO(self.file_content)

    @cached_property
    def parsed_xml(self):
        return objectify.parse(self.as_bytes_file()).getroot()

    @cached_property
    def xml_parts(self):
        return XmlPart.from_song(self)

    @property
    def title(self):
        try:
            return self.parsed_xml["movement-title"].text
        except AttributeError:
            return ugettext("Unnamed song")

    def __eq__(self, other):
        return self.sha1 == other.sha1

    def __hash__(self):
        return hash(self.sha1)

    def __str__(self):
        return self.title

    @classmethod
    def compare_sets(cls, reference_songs, found_songs):
        reference_songs = set(reference_songs)
        found_songs = set(found_songs)
        counter = itertools.count(1)
        for song in found_songs:
            song.tmp_id = next(counter)
        disappeared = reference_songs - found_songs
        appeared = found_songs - reference_songs
        disappeared_by_title = {
            song.title: song
            for song in disappeared
        }
        appeared_by_title = {
            song.title: song
            for song in appeared
        }

        common_names = set(appeared_by_title) & set(disappeared_by_title)
        updated = {
            disappeared_by_title[title]: appeared_by_title[title]
            for title in common_names
        }
        disappeared -= set(updated.values())
        appeared -= set(updated.values())

        return appeared, disappeared, updated


class FoundSong(XmlSong):

    def __init__(self, dir_path, file_name, explorer):
        self.dir_path = dir_path
        self.file_name = file_name
        self.explorer = explorer

    @property
    def path(self):
        return os.path.join(self.dir_path, self.file_name)

    def get_file_content(self):
        return self.explorer.get_content(self)

    def to_model_song(self):
        return apps.get_model("songs.Song")(name=self.title, path=self.path)


class XmlPart(object):
    def __init__(self, data, metadata, counter):
        self.metadata = metadata
        if metadata["part-name"]:
            self.name = metadata["part-name"].text
        else:
            self.name = _("Part {}").format(next(counter))
        self.data = data

    @classmethod
    def from_song(cls, song):
        counter = itertools.count(1)
        xml = song.parsed_xml
        parts_kwargs = {}
        for part_metadata in xml["part-list"]["score-part"]:
            parts_kwargs[part_metadata.get("id")] = {"metadata": part_metadata}
        for part in xml["part"]:
            parts_kwargs[part.get("id")]["data"] = part

        return [cls(counter=counter, **kwargs) for kwargs in parts_kwargs.values()]

    @property
    def first_note(self):
        """
        Returns the first note of a part (as midi_value, accidental)
        """
        for measure in self.data.measure:
            for note in measure.note:
                if hasattr(note, "rest"):
                    continue

                step = note.pitch.step.text
                octave = int(note.pitch.octave.text)

                alter_node = getattr(note.pitch, "alter", None)
                alter = int(alter_node.text) if alter_node is not None else 0
                accidental = ["flat", "natural", "sharp"][alter + 1]
                midi_value = octave * 12 + apps.get_model("songs.Part").NOTES_ORDER.index(step.lower())
                return midi_value, accidental

        return None, None

    def to_model_part(self):
        Part = apps.get_model("songs.Part")
        midi, accidental = self.first_note
        return Part(name=self.name, first_note_midi=midi, first_note_accidental=accidental)
