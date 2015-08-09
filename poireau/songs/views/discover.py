from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy as reverse
from django.apps import apps

from ..forms import FolderChoice
from ..utils.explorer import DropboxExplorer, ServerExplorer

from .dropbox import DropboxTokenMixin, DROPBOX_TOKEN_SESSION_KEY
from .song import SongMixin


class ChooseFolderView(SongMixin, FormView):
    template_name = "base/form.html"
    form_class = FolderChoice
    mode = None

    def get_form_kwargs(self):
        kwargs = super(ChooseFolderView, self).get_form_kwargs()
        kwargs["explorer"] = self.get_folder_lister()

        return kwargs

    def form_valid(self, form):
        self.request.session["DISCOVER"] = {
            "mode": self.mode,
            "folder": form.cleaned_data["folder"]
        }
        return super(ChooseFolderView, self).form_valid(form)

    def get_success_url(self):
        return reverse("songs:songs_compare")


class ChooseDropboxFolderView(DropboxTokenMixin, ChooseFolderView):
    mode = "DROPBOX"

    def get_folder_lister(self):
        return DropboxExplorer(self.dropbox_access_token)


class ChooseServerFolderView(ChooseFolderView):
    mode = "SERVER"

    def get_folder_lister(self):
        return ServerExplorer()


class SongCompareView(SongMixin, TemplateView):
    template_name = "songs/compare.html"

    def get_context_data(self, **kwargs):
        context = super(SongCompareView, self).get_context_data(**kwargs)

        mode = self.request.session["DISCOVER"]["mode"]

        if mode == "SERVER":
            explorer = ServerExplorer()
        elif mode == "DROPBOX":
            explorer = DropboxExplorer(self.request.session[DROPBOX_TOKEN_SESSION_KEY])
        else:
            return context

        context["base_folder"] = self.request.session["DISCOVER"]["folder"]
        found_songs = explorer.get_songs(self.request.session["DISCOVER"]["folder"])

        Song = apps.get_model("songs.Song")
        reference_songs = Song.objects.all()
        present_in_both, appeared, disappeared = Song.compare_sets(reference_songs, found_songs)
        context.update({
            "present_in_both": present_in_both,
            "appeared": appeared,
            "disappeared": disappeared,
        })

        return context
