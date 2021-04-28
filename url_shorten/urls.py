from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.shorten_and_pass_data, name='index'),
    path('<str:slugs>', views.url_redirect, name='redirect'),
    # path('abcdefg', views.temp_url, name='temp_redirect')
]