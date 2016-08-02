# -*- coding: utf-8 -*-

from h5game_backend import LOGGER
##pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password = "yike", socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class RedisConf:
	def __init__(self, conf):
		LOGGER.info("Init RedisConf")
		self.host = conf['host']
		self.port = conf['port']
		self.db = conf['db']
		self.password = conf['password']
		self.socket_timeout = conf['socket_timeout']
		self.socket_connect_timeout = conf['socket_connect_timeout']
		self.socket_keepalive = conf['socket_keepalive']