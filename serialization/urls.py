from django.urls import path
from .views import Serialization
from .models import *

# 创建新序列化接口只需要在下面的urlpatterns里添加即可
# 格式: path(路由, Serialization.as_view(model=数据表名, slist=序列化项目（需要与数据表的元素名严格对应）)),
urlpatterns = [
    path('user/', Serialization.as_view(model=User, slist=['name', 'mail', 'avatar', 'state', 'gender', 'bio'])),
    path('scholar/', Serialization.as_view(model=Scholar, slist=['name', 'field'])),
    path('comment/', Serialization.as_view(model=Comment, slist=['content', 'count', 'create_time'])),
    path('viewHistory/', Serialization.as_view(model=Viewhistory, slist=['field', 'user_id', 'paper_id', 'time'])),
]
