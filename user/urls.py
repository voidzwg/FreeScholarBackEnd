from django.urls import path

from user.views import *

urlpatterns = [
    path('getBaseInfo/', getBaseInfo),
    path('getFollows/', getFollows),
    path('getFollowers/', getFollowers),
    path('test/', test),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('complainSochlar/', complainSochlar),
    path('complainComment/', complainComment),
    path('complainPaper/', complainPaper),
    path('sendEmail/', sendEmail),
    path('checkCode/', checkCode),
    path('admitScholar/', admit_code),
]
