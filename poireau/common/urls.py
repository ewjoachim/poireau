from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views


urlpatterns = patterns(
    '',
    # Apps
    url(r'^songs/', include('poireau.songs.urls'), name="songs"),
    url(r'^admin/', include(admin.site.urls), name="admin"),

    # Base views
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^auth/login', views.LoginView.as_view(), name="login"),
    url(r'^auth/logout', views.LogoutView.as_view(), name="logout"),

)
