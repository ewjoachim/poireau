import os

from django import forms
from django.utils.translation import ugettext_lazy as _


class FolderChoice(forms.Form):
    folder = forms.ChoiceField(
        choices=tuple(), label=_("Folder"), help_text=_("The Dropbox folder that contains the songs."),
        required=False
    )

    def __init__(self, explorer, *args, **kwargs):
        super(FolderChoice, self).__init__(*args, **kwargs)

        self.fields["folder"].choices = [
            (dir_path, os.path.basename(dir_path) or _("Top level directory"))
            for dir_path in explorer.get_dirs()
        ]
