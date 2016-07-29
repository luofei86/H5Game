# -*- coding: utf-8 -*-
from services.DbService import get_db
from dao.GameInfoDao import *
import redis


select_sql = '''select id, title, resource_url, resource_type, possible_answer_ids, right_answer_id from h5_game_info where stauts = 0 '''
info_ids_set_key = "game:question:info:ids:set"
pool = redis.ConnectionPool(host='10.18.103.121', port=8379, db=0)

class GameInfoService:

	def __init__(self):
		self._dao = GameInfoDao()
	# def afterShare(self, tokenId, shareToContact, shareToGroup):
	# 	##用户是否还能再分享,如果不能，则分享失败

	# 	##存储用户分享的内容

	# 	return True;

	def randomGetUserNextGame(self, userToken):
		## 获取用户当前已经分享过了的
		##获取所有可以分享的游戏id
		##去重后，随机获取一个游戏内容给客户端
		return None

	def checkAnswer(self, questionId, answerId):
		return None

	def getAllInfos(self):
		# dbConn = get_db()
		# with closing(dbConn.cursor()) as cur:			
		# 	cur.execute(sql)
		# 	retlist = cur.fetchall()
		# 	doConn.commit()
		# return retlist;
		r = redis.Redis(connection_pool=pool)
		if(r):
			return r.smembers(info_ids_set_key)
		return self._dao.queryAllInfos()

