import os
import pickle

import dropbox

from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy as reverse
from django.apps import apps
from django.conf import settings
from django.db import transaction

from poireau.dropbox_sync.models import FolderSync
from poireau.dropbox_sync.views import DropboxTokenMixin
from poireau.common.utils import FilesManager

from ..forms import FolderChoice, DiscoverForm
from ..utils.xml_song import FoundSong
from .song import SongMixin
from ..models import Song


class DropboxSyncView(DropboxTokenMixin, SongMixin, FormView):
    template_name = "base/form.html"
    form_class = FolderChoice
    mode = None

    def get_form_kwargs(self):
        kwargs = super(DropboxSyncView, self).get_form_kwargs()
        self.client = dropbox.Dropbox(self.dropbox_access_token)
        entries = self.client.files_list_folder('', recursive=False).entries
        kwargs["folders"] = [entry.name for entry in entries if isinstance(entry, dropbox.files.FolderMetadata)]

        return kwargs

    def form_valid(self, form):
        FolderSync.sync_folder(
            dropbox_client=self.client,
            local_base_dir=settings.SONGS_FOLDER,
            dropbox_path="/" + form.cleaned_data["folder"]
        )
        self.success_url = reverse("songs:songs_compare")

        return super(DropboxSyncView, self).form_valid(form)


class SongCompareView(SongMixin, FormView):
    template_name = "songs/compare.html"
    form_class = DiscoverForm

    def to_session(self, songs):
        return pickle.dumps(songs)

    def from_session(self):
        return pickle.loads(self.request.session["DISCOVERED_SONGS"])

    @property
    def songs(self):
        files_manager = FilesManager()

        if hasattr(self, "_songs"):
            return self._songs
        elif "DISCOVERED_SONGS" in self.request.session:
            self._songs = self.from_session(files_manager)
        else:
            folder = settings.SONGS_FOLDER

            found_songs = [
                FoundSong(dir_path, file_name, files_manager)
                for dir_path, __, file_names in files_manager.walk(folder)
                for file_name in file_names
                if file_name.endswith(".xml")
            ]

            Song = apps.get_model("songs.Song")
            reference_songs = Song.objects.all()
            appeared, disappeared, updated = Song.compare_sets(reference_songs, found_songs)
            songs = {
                "appeared": appeared,
                "disappeared": disappeared,
                "updated": updated,
            }
            self._songs = songs
            self.to_session(songs)

        return self._songs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["songs"] = self.songs
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["songs"] = self.songs

        return context_data

    @transaction.atomic
    def form_valid(self, form):

        songs = self.songs
        disappeared_by_id = {song.id: song for song in songs["disappeared"]}
        appeared_by_id = {song.tmp_id: song for song in songs["appeared"]}

        mapping = {}
        for disappeared_field_name, appeared_tmp_id in form.cleaned_data.items():
            if not appeared_tmp_id:
                continue
            disappeared_id = int(disappeared_field_name[DiscoverForm.field_pattern.index("{}"):])
            mapping[disappeared_by_id[disappeared_id]] = appeared_by_id[appeared_tmp_id]

        songs_to_create = [
            song.to_model_song()
            for song in set(songs["appeared"]) - set(mapping.values())
        ]
        Song.objects.bulk_create(songs_to_create)

        songs_to_delete = [
            song.id
            for song in set(songs["disappeared"]) - set(mapping.keys())
        ]
        Song.objects.filter(id__in=songs_to_delete)

        songs["updated"].update(mapping)

        for new_song, old_song in songs["updated"]:
            new_song.update_from(old_song)
            new_song.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("songs:list")
