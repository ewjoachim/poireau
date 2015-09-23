

from django.conf.urls import patterns, url

from .views import song, dropbox_utils, discover


urlpatterns = patterns(
    '',
    url(r'^songs$', song.SongListView.as_view(), name='song_list'),

    url(r'^songs/discover/dropbox$', discover.ChooseDropboxFolderView.as_view(), name='songs_choose_folder_dropbox'),
    url(r'^songs/compare$', discover.SongCompareView.as_view(), name='songs_compare'),

    url(r'^song/(?P<pk>\d+)$', song.SongDetailView.as_view(), name='song_detail'),
    url(r'^song/random$', song.SongRandomView.as_view(), name='song_random'),

    url(r'^dropbox/start$', dropbox_utils.DropboxStartView.as_view(), name='dropbox_start'),
    url(r'^dropbox/finish$', dropbox_utils.DropboxFinishView.as_view(), name='dropbox_finish'),
)
