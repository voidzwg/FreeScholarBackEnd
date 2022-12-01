from datetime import time, datetime
import jwt
class Token:
    def create_token(id,password):
        token =jwt.encode({'id': id}, '123', algorithm='HS256')
        return token
    def check_token(token):
        token_ = jwt.decode(token, '123', algorithms=['HS256'])
        return token_