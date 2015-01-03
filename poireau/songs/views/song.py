from __future__ import unicode_literals

from django.views.generic import ListView

from poireau.common.views import BaseViewMixin
from ..models import Song


class SongMixin(BaseViewMixin):
    model = Song


class SongList(SongMixin, ListView):
    template_name = "songs/list.html"
