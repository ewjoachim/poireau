from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import song


urlpatterns = patterns(
    '',
    url(r'^song$', song.SongListView.as_view(), name='song_list'),
    url(r'^song/(?P<pk>\d+)$', song.SongDetailView.as_view(), name='song_detail'),
    url(r'^song/random$', song.SongRandomView.as_view(), name='song_random'),
)
