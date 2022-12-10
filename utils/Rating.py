from django_redis import get_redis_connection
import redis

expire = 60 * 60 * 24
rating_connection = get_redis_connection()
rating_connection.expire('HotWord', expire)
rating_connection.expire('HotPaper',expire)


