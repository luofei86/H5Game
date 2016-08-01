# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserPrizeInfoDao import *
from models import UserPrizeInfo
import MySQLdb
import redis
import json
import random
import string


ID_INFO_KEY = "user:prize:info:"

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password = "yike", socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class UserPrizeInfoService:
	def __init__(self):
		self._dao = UserPrizeInfoDao()

##生成用户中奖信息
	def genPrize(self, userId, activeId):
		while True:
			prizeCode = self._random_str()
			gend = self._dao.insert(userId, activeId, prizeCode)
			if gend:###可能以前中过奖了
				return self.getUserPrizeInfo(userId, activeId)			


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
			return dbValue.__dict__

		return None
####生成中奖码
	def _random_str(self, randomlength = 8):
		allCodes = list(string.ascii_letters)
		random.shuffle(allCodes)
		return ''.join(allCodes[:randomlength])

	def _buildInfoKey(self, userId, activeId):
		return ID_INFO_KEY + str(userId) + ":" + str(activeId)

	def _initCacheInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))


