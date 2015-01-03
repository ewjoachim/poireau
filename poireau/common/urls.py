from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^songs/', include('poireau.songs.urls'), name="songs"),
    url(r'^admin/', include(admin.site.urls)),
)
