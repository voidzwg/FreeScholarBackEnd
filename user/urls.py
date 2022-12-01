<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include,re_path
from user.views import *
urlpatterns = [
    path('register/',register ),
    path('login/', login),
    path('logout/', logout),
=======
from django.urls import path
from .views import *

urlpatterns = [
    path('getBaseInfo', getBaseInfo),
    path('getFollows', getFollows),
    path('getFollowers', getFollowers),
    path('test', test),
>>>>>>> c1064abb802c1e9d19d2709bfea60cc8bf7d1241
]