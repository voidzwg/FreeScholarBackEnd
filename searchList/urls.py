from django.urls import path
from .views import PaperData

urlpatterns = [
    path('PaperData/', PaperData.as_view()),
]
