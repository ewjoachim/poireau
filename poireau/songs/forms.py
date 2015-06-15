import os

from dropbox.client import DropboxClient

from django import forms
from django.utils import translation
from django.utils.translation import ugettext_lazy as _


class DropboxFolderChoice(forms.Form):
    folder = forms.ChoiceField(choices=tuple(), label=_("Folder"), help_text=_("The Dropbox folder that contains the songs."))

    def __init__(self, dropbox_access_token, *args, **kwargs):
        super().__init__(*args, **kwargs)

        client = DropboxClient(oauth2_access_token=dropbox_access_token, locale=translation.get_language())

        slash_folder = client.metadata("/")

        self.fields["folder"].choices = [
            (item["path"], os.path.basename(item["path"]))
            for item in slash_folder["contents"]
            if item["is_dir"]
        ]


