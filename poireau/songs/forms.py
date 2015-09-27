import os

from django import forms
from django.utils.translation import ugettext_lazy as _


class FolderChoice(forms.Form):
    folder = forms.ChoiceField(
        choices=tuple(), label=_("Folder"), help_text=_("The Dropbox folder that contains the songs."),
        required=False
    )

    def __init__(self, folders, *args, **kwargs):
        super(FolderChoice, self).__init__(*args, **kwargs)

        self.fields["folder"].choices = sorted([
            (dir_path, os.path.basename(dir_path))
            for dir_path in folders
        ])


class DiscoverForm(forms.Form):
    field_pattern = "song_{}"

    def __init__(self, songs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [("", _("Nothing : Delete this song"))] + [
            (song.tmp_id, song.title)
            for song in songs["appeared"]
        ]
        for song in songs["disappeared"]:
            self.fields["song_{}".format(song.id)] = forms.ChoiceField(
                choices=choices, label=_("Replace {} by :").format(song), required=False
            )
