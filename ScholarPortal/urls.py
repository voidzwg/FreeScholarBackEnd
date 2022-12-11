from django.urls import path

from .views import GetBaseInfo

urlpatterns = [
    path('GetBaseInfo/', GetBaseInfo.as_view()),
]