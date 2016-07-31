# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserPlayOriginGameInfoDao import *
import redis
import json

from h5game_backend import LOGGER

UKID_INFO_KEY = "user:play:origin:game:info:"
COUNT_KEY = "user:play:origin:count:"

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class UserPlayOriginGameInfoService:
	def __init__(self):
		self._dao = UserPlayOriginGameInfoDao()

	def addUserPlayInfo(self, userId, activeId, randomQuestionIds, playQuestionId):
		try:
			self._dao.insert(userId, activeId, randomQuestionIds, playQuestionId)
		except:
			return False
		return True

####更新id对应的result
	def modifyResultFailedCount(self, id, result, failedCount):
		self._dao.updateResultFailedCount(id, result, failedCount)
		###remove info key
		self._delInfoCache(id)

	def modifyPlayQuestionId(self, id, playQuestionId):
		self._dao.updatePlayQuestionId(id, playQuestionId)
		###remove info key
		self._delInfoCache(id)

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
			r.remove(key)

	def _buildInfoKey(self, userId, activeId):
		return UKID_INFO_KEY + str(userId) + str(activeId)		

	def _initCacheInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))


