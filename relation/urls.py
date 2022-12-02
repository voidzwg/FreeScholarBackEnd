# publish/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('test', test),
    path('getBaseInfo', getBaseInfo),
    path('getFollows', getFollows),
    path('getFollowers', getFollowers),
    path('unFocus', unFocus),
    path('getUser', getUser),
    path('setNormal', setNormal),
    path('setMute', setMute),
    path('setBan', setBan),
    path('getNum', getNum),
]