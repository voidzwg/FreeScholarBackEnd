from django.urls import path

from .models import Scholarportal
from .views import GetBaseInfo

urlpatterns = [
    path('GetBaseInfo/', GetBaseInfo.as_view(model=Scholarportal)),
]