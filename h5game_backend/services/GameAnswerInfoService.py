# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.GameAnswerInfoDao import *
import redis
import json
import random

from h5game_backend import POOL
from h5game_backend import LOGGER

info_key = "game:answer:info:"
#pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password = "yike", socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class GameAnswerInfoService:

	def __init__(self):
		self._dao = GameAnswerInfoDao()

	def getInfos(self, ids):
		if ids is None or not ids:
			return None
		results = []
		keys = []
		for id in ids:
			keys.append(self._buildInfoKey(id))
		r = redis.StrictRedis(connection_pool = POOL)
		notCacheIds = []
		if r:
			values = r.mget(keys)
			if values is None:
				notCacheIds = ids
			else:
				for index, value  in enumerate(values):
					if value is None:
						notCacheIds.append(ids[index])
					else:
						result = json.loads(value)
						results.append(result)

			if not notCacheIds:
				return results
		else:
			notCacheIds = ids
		dbValues = self._dao.queryInfos(notCacheIds)

		for dbValue in dbValues:
			key = self._buildInfoKey(dbValue.id)
			self._initInfo(r, key, dbValue)
			results.append(dbValue.__dict__)
		return results

	def _initInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))

	def _buildInfoKey(self, id):
		return info_key + str(id)
