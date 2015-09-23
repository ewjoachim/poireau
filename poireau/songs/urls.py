

from django.conf.urls import patterns, url

from .views import song, discover


urlpatterns = patterns(
    '',
    url(r'^songs$', song.SongListView.as_view(), name='song_list'),

    url(r'^songs/discover/dropbox$', discover.DropboxSyncView.as_view(), name='songs_dropbox_sync'),
    url(r'^songs/compare$', discover.SongCompareView.as_view(), name='songs_compare'),

    url(r'^song/(?P<pk>\d+)$', song.SongDetailView.as_view(), name='song_detail'),
    url(r'^song/random$', song.SongRandomView.as_view(), name='song_random'),
)
