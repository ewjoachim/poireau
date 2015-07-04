

from django.conf.urls import patterns, url

from .views import song, dropbox


urlpatterns = patterns(
    '',
    url(r'^songs$', song.SongListView.as_view(), name='song_list'),
    url(r'^songs/discover/dropbox$', song.ChooseDropboxFolderView.as_view(), name='songs_choose_folder_dropbox'),
    url(r'^songs/discover/server$', song.ChooseServerFolderView.as_view(), name='songs_choose_folder_server'),
    url(r'^songs/compare$', song.SongCompareView.as_view(), name='songs_compare'),

    url(r'^song/(?P<pk>\d+)$', song.SongDetailView.as_view(), name='song_detail'),
    url(r'^song/random$', song.SongRandomView.as_view(), name='song_random'),

    url(r'^dropbox/start$', dropbox.DropboxStartView.as_view(), name='dropbox_start'),
    url(r'^dropbox/finish$', dropbox.DropboxFinishView.as_view(), name='dropbox_finish'),
)
