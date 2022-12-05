from django.contrib import admin
from django.urls import path, include,re_path
from . import views
urlpatterns = [
    path('search/', views.publication.search),
    path('getVenueListByIdList/',views.publication.getVenueListByIdList),
    path('getKeyListByIdList/',views.publication.getKeyListByIdList),
    path('getOrgListByIdList/',views.publication.getOrgListByIdList),
]
