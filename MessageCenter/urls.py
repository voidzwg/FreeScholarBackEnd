from django.urls import path

from .views import MessageCenter

urlpatterns = [
    path("deleteMessage/", MessageCenter.as_view(post_type=1)),
    path("readMessage/", MessageCenter.as_view(post_type=2)),
    path("sendMsg/", MessageCenter.as_view(post_type=3)),
    path("getPlatMsg/", MessageCenter.as_view(get_type=1)),
    path("getMsgRec/", MessageCenter.as_view(get_type=2)),
    path("getMsgSend/", MessageCenter.as_view(get_type=3)),
]
