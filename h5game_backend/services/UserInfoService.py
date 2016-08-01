# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserInfoDao import *
import redis
import json


ID_INFO_KEY = "user:info:"
OPENID_ID_KEY = "user:openid:id:"
ID_OPENID_KEY = "user:id:openid:"

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password = "yike", socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class UserInfoService:
	def __init__(self):
		self._dao = UserInfoDao()
##获取用户中奖信息
	def getUserId(self, openId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildOpenIdReflectIdKey(openId)
			result = r.get(key)
			if result:
				return int(result)
		id = self._dao.queryIdByUk(openId)
		if id and not r:
			self._initReflectInfo(r, key, id)
		return id

	def getUserOpenId(self, id):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildIdReflectOpenIdKey(id)
			result = r.get(key)
			if result:
				return int(result)
		id = self._dao.queryOpenId(id)
		if id and not r:
			self._initReflectInfo(r, key, id)
		return id


	def _buildOpenIdReflectIdKey(self, openId):
		return OPENID_ID_KEY + openId

	def _buildIdReflectOpenIdKey(self, id):
		return ID_OPENID_KEY + str(id)

	def _initReflectInfo(self, r, key, id):
		r.set(key, id)


