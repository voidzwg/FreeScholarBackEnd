from django.urls import path

from .views import GetBaseInfo
from .models import Scholar

urlpatterns = [
    path('GetBaseInfo/', GetBaseInfo.as_view(model=Scholar)),
]