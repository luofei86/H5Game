# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserPrizeInfoDao import *
import redis
import json


ID_INFO_KEY = "user:prize:info:"

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class UserPrizeInfoService:
	def __init__(self):
		self._dao = UserPrizeInfoDao()
##获取用户中奖信息
	def getUserPrizeInfo(self, userId, activeId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildInfoKey(userId, activeId)
			cacheValue = r.get(key)
			if cacheValue:
				return json.loads(cacheValue)
		dbValue = self._dao.queryInfoByUk(userId, activeId)
		if dbValue:
			if r:
				self._initCacheInfo(r, key, dbValue)
			return dbValue.__init__

		return None

	def _buildInfoKey(self, userId, activeId):
		return ID_INFO_KEY + str(userId) + ":" + str(activeId)

	def _initCacheInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))


