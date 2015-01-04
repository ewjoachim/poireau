from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views


urlpatterns = patterns(
    '',
    url(r'^songs/', include('poireau.songs.urls'), name="songs"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomeView.as_view(), name="home"),
)
