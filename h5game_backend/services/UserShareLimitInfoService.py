# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.UserShareLimitInfoDao import *
import redis
import json

MAX_SHARE_ACCOUNT = 3
count_key = "user:share:limit:"
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

###用户分享限制服务
class UserShareLimitInfoService:

	def __init__(self):
		self._dao = UserShareLimitInfoDao()

	###增加同时检查用户是否还能进行分享,外围在调用此接口时，需要确认此次分享是不是一次重复操作
	###若此次用户可以分享，返回True，否则返回False
	def incrAndcheckLimit(self, token, activeId):
		r = redis.Redis(connection_pool = pool)
		key = self._buildCountKey(token, activeId)
		if(r):
			shareAccount = r.get(key)
			if(shareAccount is not None and int(shareAccount) >= MAX_SHARE_ACCOUNT):
				return False
			cacheValue = r.incr(key)
			if(cacheValue > MAX_SHARE_ACCOUNT):
				return False
			self._dao.insertOrIncrUpdateCount(token, activeId, MAX_SHARE_ACCOUNT)
			return True
		else:
			return self._dao.insertOrIncrUpdateCount(token, activeId, MAX_SHARE_ACCOUNT)


	###在用户点取消分享或分享失败时调用 ，用来减少用户分享次数，
	###外围在调用此接口时，需要确认此次取消分享是不是一次重复操作
	def afterShareFailed(self, token, activeId):
		r = redis.Redis(connection_pool = pool)
		key = self._buildCountKey(token, activeId)
		if(r):
			r.decr(key)
			self._dao.decrUpdateCount(token, activeId)
		else:
			self._dao.decrUpdateCount(token, activeId)

	def _buildCountKey(self, token, activeId):
		return count_key + str(token) + ":" + str(activeId)

