

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^start_oauth$', views.DropboxStartView.as_view(), name='dropbox_start'),
    url(r'^finish_oauth$', views.DropboxFinishView.as_view(), name='dropbox_finish'),
)
