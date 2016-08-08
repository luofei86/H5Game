# -*- coding: utf-8 -*-

import json
import redis

from h5game_backend import POOL
from h5game_backend import LOGGER

class RedisAdmin:
	def flushcache(self):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			r.flushall()	
