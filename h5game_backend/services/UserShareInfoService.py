# -*- coding: utf-8 -*-


from services.DbService import get_db
from dao.UserShareInfoDao import *
from models import UserShareInfo
from models import BizStatusUtils
import redis
import json
import time

from h5game_backend import POOL
#####分享地址的逻辑，用户当前玩的游戏的原生地址加上/token


# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password = "yike", socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)
####用户是否分享此个游戏
INFO_KEY = "shareinfo:id:"
USER_ACTIVEID_ID_KEY = "user:active:id:"
SHARECODE_ID_KEY ="sharecode:id:key:"
SHARED_OK = 1
SHARED_FAILED = -1
SHARED_INIT = 0

class UserShareInfoService:
	def __init__(self):
		self._dao = UserShareInfoDao()

	def getInfoByUserIdActiveId(self, userId, activeId):
		r = redis.StrictRedis(connection_pool = POOL)
		if(r):
			key = self._buildUserIdActiveIdIdKey(userId, activeId)
			result = r.get(key)
			if result is not None:
				return self.getInfo(result)
		dbValue = self._dao.queryInfoByUserIdActiveId(userId, activeId)
		if dbValue is None:
			return None
		if r:
			self._initUserIdActiveIdIdInfo(r, key, dbValue.id)
			key = self._buildInfoKey(dbValue.id)
			self._initInfo(r, key, dbValue)
		return dbValue.__dict__

	def getInfoByShareCode(self, shareCode):
		if shareCode is None:
			return None
		r = redis.StrictRedis(connection_pool = POOL)
		if(r):
			key = self._buildShareCodeIdKey(shareCode)
			result = r.get(key)
			if result is not None:
				return self.getInfo(result)
		dbValue = self._dao.queryInfoByShareCode(shareCode)
		if dbValue is None:
			return None
		if dbValue is not None and r:
			self._initShareCodeIdInfo(r, key, dbValue.id)
			key = self._buildInfoKey(dbValue.id)
			self._initInfo(r, key, dbValue)
		return dbValue.__dict__

	def getInfo(self, id):
		r = redis.StrictRedis(connection_pool = POOL)
		if(r):
			key = self._buildInfoKey(id)
			cacheValue = r.get(key)
			if cacheValue:
				return json.loads(cacheValue)
		dbValue = self._dao.queryInfo(id)
		if dbValue is None:
			return None
		if r:
			self._initInfo(r, key, dbValue)
		return dbValue.__dict__

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
		return self.getInfoByShareCode(shareCode)


	###在用户对分享有操作时，将操作结果返回
	###如果操作有效且数据库存在数据，则设备此分享码对应的游戏id
	def modifyResult(self, id, result):
		self._dao.updateResult(id, result)
		key = self._buildInfoKey(id)
		self._delInfo(key)

	def _buildInfoKey(self, id):
		return INFO_KEY + str(id)

	def _delInfo(self, key):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			r.delete(key)
	def _initInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))

	def _buildShareCodeIdKey(self, shareCode):
		return SHARECODE_ID_KEY + shareCode

	def _initShareCodeIdInfo(self, r, key, result):
		r.set(key, result)

	def _buildUserIdActiveIdIdKey(self, userId, activeId):
		return USER_ACTIVEID_ID_KEY + str(userId) + ":" + str(activeId)

	def _initUserIdActiveIdIdInfo(self, r, key, result):
		r.set(key, result)

	def _buildShareCode(self, openId):
		return openId + "_" + str(time.time()) +str(time.clock())
