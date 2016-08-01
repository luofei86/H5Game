# -*- coding: utf-8 -*-


from services.DbService import get_db
from dao.UserShareInfoDao import *
from models import UserShareInfo
import redis
import json
import time

#####分享地址的逻辑，用户当前玩的游戏的原生地址加上/token


pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)
SHARECODE_ACTIVEID_KEY="sharecode:activeid:"
USER_SHARED_ID = "user:shared:id:"
SHARED_OK = 1
SHARED_FAILED = -1
SHARED_INIT = 0

class UserShareInfoService:
	def __init__(self):
		self._dao = UserShareInfoDao()

	def getShareActiveId(self, shareCode):
		if shareCode is None:
			return None
		r = redis.Redis(connection_pool = pool)
		if(r):
			key = self._buildShareActiveIdKey(shareCode)			
			result = r.get(key)
			if result is None:
				return None
			return int(result)
		else:
			return self._dao.queryActiveIdByShareCode(shareCode)

	def userShared(self, userId, activeId):
		r = redis.Redis(connection_pool = pool)
		if r:
			key = self._buildUserSharedActiveKey(userId, activeId)
			cacheValue = r.exists(key)
			if cacheValue is not None:
				return cacheValue
		dbValue = self._dao.queryId(userId, activeId, SHARED_OK)
		if dbValue is not None:
			if r:
				self._initSharedValue(r, key, dbValue)
			return True
		return False


	#添加分享，在确认分享数量没问题后，调用此接口返回相关信息
	def genShareInfo(self, userId, openId, activeId, activeUrl):
		shareCode = self._buildShareCode(openId)
		if str(activeUrl).endswith("/"):
			shareUrl = activeUrl + shareCode
		else:
			shareUrl = activeUrl + "/" + shareCode
		title = u"我发现一个好玩的游戏，你也快来吧"
		content =u"精彩一夏奥运"
		self._dao.insert(userId, activeId, shareCode, shareUrl, title, content)
		userShareInfo = UserShareInfo(userId, activeId, shareCode, shareUrl, title, content, 0)
		return userShareInfo

	###在用户对分享有操作时，将操作结果返回
	###如果操作有效且数据库存在数据，则设备此分享码对应的游戏id
	def afterShare(self, shareCode, result):
		self._dao.updateResult(shareCode, result)
		if(int(result) == 1):
			activeId = self._dao.queryActiveIdByShareCode(shareCode)
			if activeId is not None:
				r = redis.Redis(connection_pool = pool)
				if(r):
					key = self._buildShareActiveIdKey(shareCode)			
					r.set(key, activeId)
				return True
			else:
				return False
		return False

	def _buildUserSharedActiveKey(self, userId, activeId):
		return USER_SHARED_ID + str(userId) + ":" + str(activeId)

	def _initSharedValue(self, r, key, value):
		r.set(key, value)

	def _buildShareActiveIdKey(self, shareCode):
		return SHARECODE_ACTIVEID_KEY + shareCode

	def _buildShareCode(self, openId):
		return openId + "_" + str(time.time()) +str(time.clock())
