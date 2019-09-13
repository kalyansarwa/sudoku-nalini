""" This module contains paths for Games """
from django.conf.urls import url
from games import views

app_name = 'games'

urlpatterns = [
    url(r'^(?P<gid>\d+)$', views.games, name='games'),
    url(r'^$', views.games, name='games'),
]
