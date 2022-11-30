from django.urls import path
from .views import *

urlpatterns = [
    path('getBaseInfo', getBaseInfo),
    path('getFollows', getFollows),
    path('getFollowers', getFollowers),
    path('test', test),
]