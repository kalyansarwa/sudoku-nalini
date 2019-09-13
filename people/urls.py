""" This module contains paths for People """
from django.conf.urls import url
from people import views

app_name = 'people'

urlpatterns = [
    url(r'^register$', views.register, name='register'),
]
