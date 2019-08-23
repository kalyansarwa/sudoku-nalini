""" This module contains paths for People """
from django.conf.urls import url
from people import views

urlpatterns = [
    url(r'^register$', views.register, name='register'),
]
