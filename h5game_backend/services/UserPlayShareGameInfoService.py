# -*- coding: utf-8 -*-

from services.DbService import get_db
from dao.UserPlayShareGameInfoDao import *
import redis
import json

from h5game_backend import POOL
from h5game_backend import LOGGER

UK_INFO_KEY = "user:play:share:game:info:"
USER_LAST_PLAY_KEY = "user:play:share:game:last:info:"
COUNT_KEY = "user:play:share:count:"

# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password = "yike", socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class UserPlayShareGameInfoService:
	def __init__(self):
		self._dao = UserPlayShareGameInfoDao()

	def addUserPlayInfo(self, userId, activeId, shareCode, randomQuestionIds, playQuestionId):
		randomQuestionIdsStr = ', '.join(str(x) for x in randomQuestionIds)
		try:
			self._dao.insert(userId, activeId, shareCode, randomQuestionIdsStr, playQuestionId)
			self._incrCount(userId, activeId)
			return self.getInfo(userId, activeId, shareCode)
		except:
			return None
	####更新id对应的result
	def modifyResult(self, id, userId, activeId, shareCode, result):
		self._dao.updateResult(id, result)
		self._delInfoCache(userId, activeId, shareCode)

	def modifyPlayQuestionId(self, id, userId, activeId, shareCode, playQuestionId):
		self._dao.updatePlayQuestionId(id, playQuestionId)		
		self._delInfoCache(userId, activeId, shareCode)

	def getUserlastPlayInfo(self, userId, activeId):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildLastInfoKey(userId, activeId)
			cacheValue = r.get(key)
			if cacheValue:
				return json.loads(cacheValue)
		dbValue = self._dao.queryLastInfo(userId, activeId)
		if dbValue:
			if r:
				self._initCacheInfo(r, key, dbValue)
			return dbValue.__dict__
		return None

	def _buildLastInfoKey(self, userId, activeId):
		return USER_LAST_PLAY_KEY + str(userId) + str(activeId)

	def getInfo(self, userId, activeId, shareCode):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildInfoKey(userId, activeId, shareCode)
			cacheValue = r.get(key)
			if cacheValue:
				return json.loads(cacheValue)
		dbValue = self._dao.queryInfoByUk(userId, activeId, shareCode)
		if dbValue:
			if r:
				self._initCacheInfo(r, key, dbValue)
			return dbValue.__dict__
		return None


	def countUserPlay(self, userId, activeId):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildCountKey(userId, activeId)
			cacheValue = r.get(key)
			if cacheValue:
				return int(cacheValue)
		count = self._dao.count(userId, activeId)
		if count:
			if r:
				self._initCount(r, key, count)
			return count
		return 0

	def _incrCount(self, userId, activeId):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildCountKey(userId, activeId)
			r.incr(key)

	def _initCount(self, r, key, count):
		r.set(key, count)

	def _initCacheInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))


	def _buildCountKey(self, userId, activeId):
		return COUNT_KEY + str(userId) + ":" + str(activeId)

	def _delInfoCache(self, userId, activeId, shareCode):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildInfoKey(userId, activeId, shareCode)
			r.delete(key)

	def _buildInfoKey(self, userId, activeId, shareCode):
		return UK_INFO_KEY + str(userId) + str(activeId) + shareCode		


