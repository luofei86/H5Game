# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserInfoDao import *
import redis
import json

from h5game_backend import POOL

ID_INFO_KEY = "user:info:"
UNIONID_ID_KEY = "user:unionid:id:"
ID_UNIONID_KEY = "user:id:unionid:"

class UserInfoService:
	def __init__(self):
		self._dao = UserInfoDao()

	def addInfo(self, unionId):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildUnionIdReflectIdKey(unionId)
			result = r.get(key)
			if result:
				return
		self._dao.insert(unionId)

##获取用户中奖信息
	def getUserId(self, unionId):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildUnionIdReflectIdKey(unionId)
			result = r.get(key)
			if result:
				return int(result)
		id = self._dao.queryIdByUk(unionId)
		if id and not r:
			self._initReflectInfo(r, key, id)
		return id

	def getUserUnionId(self, id):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildIdReflectUnionIdKey(id)
			result = r.get(key)
			if result:
				return int(result)
		id = self._dao.queryUnionId(id)
		if id and not r:
			self._initReflectInfo(r, key, id)
		return id


	def _buildUnionIdReflectIdKey(self, unionId):
		return UNIONID_ID_KEY + unionId

	def _buildIdReflectUnionIdKey(self, id):
		return ID_UNIONID_KEY + str(id)

	def _initReflectInfo(self, r, key, id):
		r.set(key, str(id))


