
from django.contrib import admin
from django.urls import path, include,re_path
from user.views import *
from django.urls import path

urlpatterns = [
    path('getBaseInfo', getBaseInfo),
    path('getFollows', getFollows),
    path('getFollowers', getFollowers),
    path('test', test),
    path('register/',register ),
    path('login/', login),
    path('logout/', logout),
]