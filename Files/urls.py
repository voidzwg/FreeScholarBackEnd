from django.urls import path

from .models import User, Favorites
from .views import Media

urlpatterns = [
    path("set_avatar/", Media.as_view(post_type=1, model=User)),
    path("set_cover/", Media.as_view(post_type=2, model=Favorites)),
]
