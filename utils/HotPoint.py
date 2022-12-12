from django_redis import get_redis_connection
import redis

expire = 60 * 60 * 24 * 7
scholar_connection = get_redis_connection()
scholar_connection.expire('HotScholar', expire)
