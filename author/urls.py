from django.urls import path, include,re_path
from . import views

urlpatterns = [
    path('getAuthor/', views.author.getAuthor),
    path('count/', views.author.count),
]
