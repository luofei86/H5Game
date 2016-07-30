# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.GameQuestionInfoDao import *
import redis
import json

select_sql = '''select id, title, resource_url, resource_type, possible_answer_ids, right_answer_id from h5_game_info where stauts = 0 '''
info_ids_set_key = "game:question:info:ids:set"
info_key = "game:question:info:"
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, socket_timeout=5, socket_connect_timeout=1, socket_keepalive=7200)

class GameQuestionInfoService:

	def __init__(self):
		self._dao = GameQuestionInfoDao()
	# def afterShare(self, tokenId, shareToContact, shareToGroup):
	# 	##用户是否还能再分享,如果不能，则分享失败

	# 	##存储用户分享的内容

	# 	return True

	def randomGetUserNextGame(self, userToken):
		## 获取用户当前已经分享过了的
		##获取所有可以分享的游戏id
		##去重后，随机获取一个游戏内容给客户端
		return None

	###检查答案
	def checkAnswer(self, questionId, answerId):
		r = redis.Redis(connection_pool=pool)
		key = self._buildInfoKey(questionId)
		if(r):
			cacheValue = r.get(key)
			if(cacheValue is not None):
				result = json.loads(cacheValue)
				return answerId == result['rightAnswerId']
		result = self._dao.queryInfo(questionId)
		if(result is None):
			return false
		self._initInfo(questionId, result, r)
		return answerId == result.rightAnswerId

	def _initInfo(self, id, result, r):
		key = self._buildInfoKey(id)
		r.set(key, json.dumps(result.__dict__))

	def _buildInfoKey(self, id):
		return info_key + str(id)

	def getAllInfos(self):
		# dbConn = get_db()
		# with closing(dbConn.cursor()) as cur:			
		# 	cur.execute(sql)
		# 	retlist = cur.fetchall()
		# 	doConn.commit()
		# return retlist
		# r = redis.Redis(connection_pool=pool)
		# if(r):
		# 	return r.smembers(info_ids_set_key)
		return self._dao.queryAllInfos()

