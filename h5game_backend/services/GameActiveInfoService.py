# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.GameActiveInfoDao import *
import redis
import json


ID_INFO_KEY = "game:active:info:"
SIGNWORD_ID_KEY = "game:active:signword:id:"
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class GameActiveInfoService:
	def __init__(self):
		self._dao = GameActiveInfoDao()

	def getInfo(self, id):
		r = redis.Redis(connection_pool=pool)
		if(r):
			key = self._buildInfoKey(id)
			cacheValue = r.get(key)
			if(cacheValue is not None):
				result = json.loads(cacheValue)
				return result
		result = self._dao.queryInfo(id)

		if result is not None and r is not None:
			self._initInfo(id, result, r)

		return result.__dict__

	def getInfoBySignWord(self, signWord):
		r = redis.Redis(connection_pool = pool)
		if(r):
			key = self._buildSignWordInfoIdKey(signWord)
			cacheValue = r.get(key)
			if cacheValue is not None:
				id = int(cacheValue)
				return self.getInfo(id)

		result = self._dao.queryInfoByUk(signWord)
		if(result is not None and r is not None):
			self._initInfo(signWord.id, signWord, r)
		return result.__dict__

	def _buildSignWordInfoIdKey(self, signWord):
		return SIGNWORD_ID_KEY + signWord

	def _buildInfoKey(self, id):
		return ID_INFO_KEY + str(id)

	def _initInfo(self, id, result, r):
		key = self._buildInfoKey(id)
		r.set(key, json.dumps(result.__dict__))
		key = self._buildSignWordInfoIdKey(result.signWord)
		r.set(key, id)

