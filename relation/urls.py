# publish/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('test', test),
    path('getBaseInfo', getBaseInfo),
    path('getFollows', getFollows),
    path('getFollowers', getFollowers),
    path('unFocus', unFocus),
    path('focus', focus),
    path('like', like),
    path('getUser', getUser),
    path('setNormal', setNormal),
    path('setMute', setMute),
    path('setBan', setBan),
    path('getNum', getNum),
    path('getUserItem', getUserItem),
    path('getScholarItem', getScholarItem),
    path('editInfo', editInfo),
    path('changePwd', changePwd),

    path('getReportAll',getReportAll),
    path('getComplainAll',getComplainAll),
    path('getRecentRecord',getRecentRecord),

    path('getFavorites', getFavorites),
    path('newFavorites', newFavorites),
    path('set_avatar/', set_avatar),
    path('getCollectFavorites', getCollectFavorites),
    path('collectFavorites', collectFavorites),

]