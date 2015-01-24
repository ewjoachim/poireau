from __future__ import unicode_literals

from django.views.generic import ListView

from poireau.common.views import BaseViewMixin
from poireau.songs.models import Song


class SongMixin(BaseViewMixin):
    model = Song


class SongListView(SongMixin, ListView):
    template_name = "songs/list.html"
    menu_list = ["songs"]

    def get_queryset(self):
        return super(SongListView, self).get_queryset().order_by("path")
