# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserPlayShareGameInfoDao import *
import redis
import json


UK_INFO_KEY = "user:play:share:game:info:"
COUNT_KEY = "user:play:share:count:"

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class UserPlayShareGameInfoService:
	def __init__(self):
		self._dao = UserPlayShareGameInfoDao()

	def addUserPlayInfo(self, userId, activeId, shareCode, randomQuestionIds, playQuestionId):
		self._dao.insert(userId, activeId, shareCode, randomQuestionIds, playQuestionId)
		self._incrCount(userId, activeId, shareCode)

	def getUserPlayInfo(self, userId, activeId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildInfoKey(userId, activeId, shareCode)
			result = r.get(key)
			if result:
				return json.loads(cacheValue)
		dbValue = self._dao.queryInfoByUk(userId, activeId, shareCode)
		if dbValue:
			if r:
				self._initCacheInfo(r, key, dbValue)
			return dbValue.__init__
		return None


	def countUserPlay(self, userId, activeId, shareCode):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildCountKey(userId, activeId, shareCode)
			result = r.get(key)
			if result:
				return int(result)
		count = self._dao.count(userId, activeId, shareCode)
		if count:
			if r:
				self._initCount(r, key, count)
		return count

		return None


	def _incrCount(self, userId, activeId, shareCode):
		r = redis.Redis(connection_pool = pool)		
		if r:
			key = self._buildCountKey(userId, activeId, shareCode)
			r.incr(key)

	def _initCount(self, r, key, count):
		r.set(key, count)

	def _initCacheInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))


	def _buildCountKey(self, userId, activeId, shareCode):
		return COUNT_KEY + str(userId) + ":" + str(activeId) + ":" + shareCode


	def _buildInfoKey(self, userId, activeId, shareCode):
		return UKID_INFO_KEY + str(userId) + str(activeId) + shareCode		


