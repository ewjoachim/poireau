from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import song


urlpatterns = patterns(
    '',
    url(r'^song/list$', song.ListView.as_view(), name='song_list'),
)
