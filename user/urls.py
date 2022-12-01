from django.contrib import admin
from django.urls import path, include,re_path
from user.views import *
urlpatterns = [
    path('register/',register ),
    path('login/', login),
    path('logout/', logout),
]