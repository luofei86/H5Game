# -*- coding: utf-8 -*-

from services.DbService import get_db
from dao.UserInfoDao import *
import redis
import json

from h5game_backend import POOL
from h5game_backend import LOGGER

ID_INFO_KEY = "user:info:"
OPENID_ID_KEY = "user:openId:id:"
ID_OPENID_KEY = "user:id:openId:"

class UserInfoService:
	def __init__(self):
		self._dao = UserInfoDao()

	def addInfo(self, weiXinInfo):
		LOGGER.debug(str(weiXinInfo))
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildOpenIdReflectIdKey(weiXinInfo['openid'])
			result = r.get(key)
			if result:
				return
		self._dao.insert(weiXinInfo['openid'], weiXinInfo['unionid'], weiXinInfo['nickname'], \
						 weiXinInfo['sex'], weiXinInfo['language'], weiXinInfo['city'], \
						 weiXinInfo['province'], weiXinInfo['country'], weiXinInfo['headimgurl'])
##获取用户中奖信息
	def getUserId(self, openId):
		r = redis.StrictRedis(connection_pool = POOL)
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
		r = redis.StrictRedis(connection_pool = POOL)
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
		r.set(key, str(id))


