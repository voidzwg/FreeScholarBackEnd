<<<<<<< HEAD
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
]
=======
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
]
>>>>>>> 68790d58aacfa9d7919048a30371d0f8f98d665e
