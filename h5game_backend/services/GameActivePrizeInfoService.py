# -*- coding: utf-8 -*-

from services.DbService import get_db
from dao.GameActivePrizeInfoDao import *
import redis
import json

ID_INFO_KEY = "game:active:prize:info:"
ACTIVE_ID_PRIZE_SORTEDSET_KEY = "game:active:prize:sorted:ids:"
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password = "yike", socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class GameActivePrizeInfoService:
	def __init__(self):
		self._dao = GameActivePrizeInfoDao()

	def getInfosByActiveId(self, activeId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildActiveIdIdsSortedKey(activeId)
			caches = r.zrange(key, 0, -1)
			if not (caches is None or not caches):
				ids = caches
				return self.getInfos(ids)
		dbValues = self._dao.queryInfosByActiveId(activeId)
		results = []

		for dbValue in dbValues:
			self._initInfo(dbValue.id, dbValue, r)
			results.append(dbValue.__dict__)
		self._initSortedSet(activeId, dbValues)
		return results

##初始化active-id level sorted set
	def _initSortedSet(self, activeId, dbValues):
		r = redis.Redis(connection_pool = pool)		
		if r:
			key = self._buildActiveIdIdsSortedKey(activeId)
			for dbValue in dbValues:
				r.zadd(key, dbValue.id, int(dbValue.level))

####将保证按给定的ids序返回
	def getInfos(self, ids):
		if ids is None or not ids:
			return None
		results = []
		keys = []
		for id in ids:
			keys.append(self._buildInfoKey(id))
		r = redis.Redis(connection_pool = pool)
		notCacheIds = []
		if r:
			values = r.mget(keys)
			if values is None:
				notCacheIds = ids
			else:
				for index, value in enumerate(values):
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
			self._initInfo(dbValue.id, dbValue, r)
			results.append(dbValue.__dict__)

		return results

	def getInfo(self, id):
		r = redis.Redis(connection_pool = pool)
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

	def _buildInfoKey(self, id):
		return ID_INFO_KEY + str(id)


	def _buildActiveIdIdsSortedKey(self, id):
		return ACTIVE_ID_PRIZE_SORTEDSET_KEY + str(id)

	def _initInfo(self, id, result, r):
		if r is None:
			return
		key = self._buildInfoKey(id)
		r.set(key, json.dumps(result.__dict__))

