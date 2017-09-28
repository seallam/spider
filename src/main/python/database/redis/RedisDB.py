import redis


class RedisDB:
	_redis = None

	def __init__(self):
		pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=3)
		self._redis = redis.Redis(connection_pool=pool)

	def get_redis(self):
		return self._redis
