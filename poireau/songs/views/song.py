

from django.views.generic import View, ListView, DetailView, FormView
from django import http
from django.core.urlresolvers import reverse_lazy as reverse

from poireau.common.views import BaseLoggedViewMixin
from poireau.songs.models import Song
from poireau.songs.views.dropbox import DropboxTokenMixin

from ..forms import DropboxFolderChoice


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


class SongDiscoverView(DropboxTokenMixin, SongMixin, FormView):
    template_name = "songs/discover.html"
    form_class = DropboxFolderChoice

    def get_form_kwargs(self):
        kwargs = super(SongDiscoverView, self).get_form_kwargs()
        kwargs.update({"dropbox_access_token": self.dropbox_access_token})
        return kwargs
