from django.contrib import admin
from django.urls import path, include,re_path
from . import views
urlpatterns = [
    path('search/', views.publication.search),
    path('GetWord/', views.publication.GetWord),
    path('HotPaper/', views.publication.HotPaper),
    path('HotWord/', views.publication.HotWord),
    path('LikePaper/', views.publication.LikePaper),
    path('ReadPaper/', views.publication.ReadPaper),
    path('CollectPaper/', views.publication.CollectPaper),
    path('getVenueListByIdList/',views.publication.getVenueListByIdList),
    path('getKeyListByIdList/',views.publication.getKeyListByIdList),
    path('getOrgListByIdList/',views.publication.getOrgListByIdList),
    path('getPaperByIdList/',views.publication.getPaperByIdList),
    path('addPub/',views.publication.addPub),
    path('getPaperById/', views.publication.getPaperById),
    path('recommend/', views.publication.recommend),
]

