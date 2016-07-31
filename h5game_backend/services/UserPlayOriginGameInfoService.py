# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserPlayOriginGameInfoDao import *
import redis
import json


UKID_INFO_KEY = "user:play:origin:game:info:"
COUNT_KEY = "user:play:origin:count:"

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class UserPlayOriginGameInfoService:
	def __init__(self):
		self._dao = UserPlayOriginGameInfoDao()

	def addUserPlayInfo(self, userId, activeId, randomQuestionIds, playQuestionId):
		self._dao.insert(userId, activeId, randomQuestionIds, playQuestionId)
		self._incrCount(userId, activeId)

	def getUserPlayInfo(self, userId, activeId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildInfoKey(userId, activeId)
			result = r.get(key)
			if result:
				return json.loads(cacheValue)
		dbValue = self._dao.queryInfoByUk(userId, activeId)
		if dbValue:
			if r:
				self._initCacheInfo(r, key, dbValue)
			return dbValue.__init__
		return None


	def countUserPlay(self, userId, activeId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildCountKey(userId, activeId)
			result = r.get(key)
			if result:
				return int(result)
		count = self._dao.count(userId, activeId)
		if count:
			if r:
				self._initCount(r, key, count)
		return count

		return None

	def _buildCountKey(self, userId, activeId):
		return COUNT_KEY + str(userId) + str(activeId)

	def __buildInfoKey(self, userId, activeId):
		return UKID_INFO_KEY + str(userId) + str(activeId)		

	def _incrCount(self, userId, activeId):
		r = redis.Redis(connection_pool = pool)		
		if r:
			key = self._buildCountKey(userId, activeId)
			r.incr(key)

	def _initCount(self, r, key, count):
		r.set(key, count)

	def _initCacheInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))


