import time

import jwt
from django_redis import get_redis_connection

from FreeScholarBackEnd.settings import SECRETS


class Authentication:
    redis_connection = get_redis_connection()
    expire = 60 * 1 * 1

    @staticmethod
    def create_token(uid, admin=False):
        cls = Authentication
        token_expire = int(time.time()) + cls.expire
        payload = {
            'id': uid,
            'admin': admin,
            'exp': token_expire
        }
        token_obj = cls.generate_jwt_token(payload)
        cls.redis_connection.set(uid, token_obj)
        return token_obj

    @staticmethod
    def authentication(request_dict):
        cls = Authentication
        fail_json_msg = {
            'errno': -1,
            'msg': "token已失效，请重新登录"
        }
        fail_json_msg2 = {
            'errno': -2,
            'msg': "未收到token令牌"
        }
        try:
            token = request_dict.get('HTTP_JWT')
        except KeyError:
            return True, fail_json_msg2
        payload = cls.verify_jwt_token(token)
        if payload is None:
            return True, fail_json_msg
        else:
            token_in_redis = cls.redis_connection.get(payload.get('id'))
            if token_in_redis is None or token != token_in_redis.decode():
                return True, fail_json_msg
        return False, payload

    @staticmethod
    def logout(uid):
        cls = Authentication
        cls.redis_connection.delete(uid)

    @staticmethod
    def generate_jwt_token(payload):
        if isinstance(payload, dict):
            token = jwt.encode(payload, SECRETS.get('JWT_SECRET'), algorithm=SECRETS.get('JWT_ALGORITHM'))
            return token
        return None

    @staticmethod
    def verify_jwt_token(token):
        try:
            payload = jwt.decode(token, SECRETS.get('JWT_SECRET'), algorithms=[SECRETS.get('JWT_ALGORITHM')])
        except jwt.PyJWTError:
            return None
        if int(payload.get('exp')) > int(time.time()):
            return payload
        return None
