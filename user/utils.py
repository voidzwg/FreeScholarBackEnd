from datetime import time, datetime
import jwt
from django.utils import timezone
import datetime
class Token:
    def create_token(id,password):
        # 返回时间格式的字符串
        now=datetime.datetime.now()
        now_time_str = now.strftime("%Y.%m.%d %H:%M:%S")
        token =jwt.encode({'id': id,'time':now_time_str}, '123', algorithm='HS256')
        return token
    def check_token(token):
        token_ = jwt.decode(token, '123', algorithms=['HS256'])
        return token_