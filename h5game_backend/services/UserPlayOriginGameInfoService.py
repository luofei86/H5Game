# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserPlayOriginGameInfoDao import *
import redis
import json

from h5game_backend import LOGGER

UKID_INFO_KEY = "user:play:origin:game:info:"
COUNT_KEY = "user:play:origin:count:"

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password = "yike", socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class UserPlayOriginGameInfoService:
	def __init__(self):
		self._dao = UserPlayOriginGameInfoDao()

	def addUserPlayInfo(self, userId, activeId, randomQuestionIds, playQuestionId):		
		randomQuestionIdsStr = ', '.join(str(x) for x in randomQuestionIds)
		try:			
			self._dao.insert(userId, activeId, randomQuestionIdsStr, playQuestionId)
			return self.getInfo(userId, activeId)
		except:
			return None
#####
	def modifyResult(self, id, userId, activeId, result):
		return self._dao.updateResult(id, result)
		self._delInfoCache(userId, activeId)

####更新id对应的result
	def modifyResultFailedCount(self, id, userId, activeId, result, failedCount):
		self._dao.updateResultFailedCount(id, result, failedCount)
		###remove info key
		self._delInfoCache(userId, activeId)

	def modifyPlayQuestionId(self, id, userId, activeId, playQuestionId):
		self._dao.updatePlayQuestionId(id, playQuestionId)
		###remove info key
		self._delInfoCache(userId, activeId)

	def getInfo(self, userId, activeId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildInfoKey(userId, activeId)
			result = r.get(key)
			if result:
				return json.loads(result)
		dbValue = self._dao.queryInfo(userId, activeId)
		if dbValue:
			if r:
				self._initCacheInfo(r, key, dbValue)
			return dbValue.__dict__
		return None

	def _delInfoCache(self, userId, activeId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildInfoKey(userId, activeId)
			r.delete(key)

	def _buildInfoKey(self, userId, activeId):
		return UKID_INFO_KEY + str(userId) + str(activeId)		

	def _initCacheInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))


