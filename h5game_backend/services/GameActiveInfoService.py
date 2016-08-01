# -*- coding: utf-8 -*-
from services.DbService import get_db
from utils.JsonEncoder import *
from dao.GameActiveInfoDao import *
import redis
import json

from h5game_backend import LOGGER


ID_INFO_KEY = "game:active:info:"
SIGNWORD_ID_KEY = "game:active:signword:id:"
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password="yike", db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

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
			self._initInfo(r, key, result)

		return result.__dict__

	def getInfoBySignWord(self, signWord):
		r = redis.Redis(connection_pool = pool)
		if r:
			LOGGER.info("Connection")
			key = self._buildSignWordInfoIdKey(signWord)
			cacheValue = r.get(key)
			if cacheValue is not None:
				id = int(cacheValue)
				return self.getInfo(id)
		else:
			LOGGER.info("not connection")
		result = self._dao.queryInfoByUk(signWord)
		if(result is not None and r is not None):
			infoKey = self._buildInfoKey(result.id)
			self._initInfo(r, infoKey, result)
			self._initSignWordIdInfo(r, key, result.id)
		return result.__dict__

	def _buildSignWordInfoIdKey(self, signWord):
		return SIGNWORD_ID_KEY + signWord

	def _buildInfoKey(self, id):
		return ID_INFO_KEY + str(id)

	def _initInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__, cls = JsonEncoder))

	def _initSignWordIdInfo(self, r, key, id):
		r.set(key, id)

