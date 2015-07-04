

from django.views.generic import View, ListView, DetailView, FormView, TemplateView
from django import http
from django.core.urlresolvers import reverse_lazy as reverse
from django.conf import settings

from poireau.common.views import BaseLoggedViewMixin
from poireau.songs.models import Song
from poireau.songs.views.dropbox import DropboxTokenMixin, DROPBOX_TOKEN_SESSION_KEY

from ..forms import FolderChoice
from ..utils import DropboxFolderExplorer, ServerFolderExplorer


class SongMixin(BaseLoggedViewMixin):
    model = Song


class SongListView(SongMixin, ListView):
    template_name = "songs/list.html"
    menu_list = ["songs"]

    def get_queryset(self):
        return super(SongListView, self).get_queryset().order_by("path")


class SongDetailView(SongMixin, DetailView):
    template_name = "songs/detail.html"
    menu_list = ["songs"]


class SongRandomView(SongMixin, View):

    def get(self, request):
        song = Song.objects.order_by("?").first()
        if song:
            return http.HttpResponseRedirect(song.get_absolute_url())
        else:
            return http.HttpResponseRedirect(reverse("songs:song_list"))


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
        return DropboxFolderExplorer(self.dropbox_access_token)


class ChooseServerFolderView(ChooseFolderView):
    mode = "SERVER"

    def get_folder_lister(self):
        return ServerFolderExplorer()


class SongCompareView(SongMixin, TemplateView):
    template_name = "songs/compare.html"

    def get_context_data(self, **kwargs):
        context = super(SongCompareView, self).get_context_data(**kwargs)

        mode = self.request.session["DISCOVER"]["mode"]

        if mode == "SERVER":
            explorer = ServerFolderExplorer()
        elif mode == "DROPBOX":
            explorer = DropboxFolderExplorer(self.request.session[DROPBOX_TOKEN_SESSION_KEY])
        else:
            return context

        context["base_folder"] = self.request.session["DISCOVER"]["folder"]
        context["songs"] = explorer.get_songs(self.request.session["DISCOVER"]["folder"])

        return context
