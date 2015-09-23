import os

import dropbox

from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy as reverse
from django.apps import apps
from django.conf import settings

from poireau.dropbox_sync.models import FolderSync

from ..forms import FolderChoice, DiscoverForm

from ..utils.xml_song import FoundSong
from .dropbox_utils import DropboxTokenMixin
from .song import SongMixin


class ChooseDropboxFolderView(DropboxTokenMixin, SongMixin, FormView):
    template_name = "base/form.html"
    form_class = FolderChoice
    mode = None

    def get_form_kwargs(self):
        kwargs = super(ChooseDropboxFolderView, self).get_form_kwargs()
        self.client = dropbox.Dropbox(self.dropbox_access_token)
        entries = self.client.files_list_folder('/', recursive=False).entries
        kwargs["folders"] = [entry.name for entry in entries if isinstance(entry, dropbox.FolderMetaData)]

        return kwargs

    def form_valid(self, form):
        FolderSync.sync_folder(
            dropbox_client=self.client,
            local_base_dir=settings.SONGS_FOLDER,
            dropbox_path="/" + form.cleaned_data["folder"]
        )
        self.success_url = reverse("songs:songs_compare", kwargs={"folder": form.cleaned_data["folder"]})

        return super(ChooseDropboxFolderView, self).form_valid(form)


class SongCompareView(SongMixin, FormView):
    template_name = "songs/compare.html"
    form_class = DiscoverForm

    @property
    def songs(self):
        if hasattr(self, "_songs"):
            return self._songs
        elif "songs" in self.request.session["DISCOVER"]:
            self._songs = self.request.session["DISCOVER"]["songs"]
        else:
            folder = self.kwargs["folder"]
            songs = [
                FoundSong(os.path.join(self.base_folder, folder, dir_path), file_name, self)
                for dir_path, __, file_names in os.walk(folder)
                for file_name in file_names
                if file_name.endswith(".xml")
            ]
            found_songs = self.kwargs[folder]

            Song = apps.get_model("songs.Song")
            reference_songs = Song.objects.all()
            appeared, disappeared, updated = Song.compare_sets(reference_songs, found_songs)
            songs = {
                "appeared": appeared,
                "disappeared": disappeared,
                "updated": updated,
            }
            self._songs = songs
            self.request.session["DISCOVER"]["songs"] = songs

        return self._songs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["songs"] = self.songs
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SongCompareView, self).get_context_data(**kwargs)
        context["base_folder"] = self.request.session["DISCOVER"]["folder"]
        context.update(self.songs)

        return context
