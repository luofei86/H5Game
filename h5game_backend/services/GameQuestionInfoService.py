# -*- coding: utf-8 -*-

from services.DbService import get_db
from dao.GameQuestionInfoDao import *
import redis
import json
import random

from h5game_backend import POOL

ACTIVEID_QUESTIONID_SET_PREFIX_KEY = "game:active:question:ids:set:"
info_key = "game:question:info:"

RANDOM_QUESTION_COUNT = 5

class GameQuestionInfoService:

	def __init__(self):
		self._dao = GameQuestionInfoDao()

####随机用户答题目
####获取此活动下所有的题目，随机选取5道题目做为当前用户此次答题用到的题目,返回5道题目的id及第一道题目的内容
	def randomAndGetUserFirstQuestion(self, activeId):
		playQuestionIds = []		
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = self._buildActiveQuestionIds(activeId)
			caches = r.smembers(key)
			if not caches:
				if len(caches) <= RANDOM_QUESTION_COUNT:
					playQuestionIds = caches
				else:
					##random get RANDOM_QUESTION_COUNT
					playQuestionIds = self._randomIds(caches)
					
		if not playQuestionIds:
			questionIds = self._dao.queryIds(activeId)
			if questionIds is None or not questionIds:
				return None, None
			self._initActiveQuestionSet(activeId, questionIds, r)
			playQuestionIds = self._randomIds(questionIds)
		if not playQuestionIds:
			return None, None
		playId = playQuestionIds[0]
		result = self.getInfo(playId)
		return result, playQuestionIds

	def _randomIds(self, ids, length = 5):
		if not ids:
			return None
		if len(ids) < length:
			return None
		return random.sample(ids, length)

	def _initActiveQuestionSet(self, activeId, ids, r):
		if(r is None):
			return
		key = self._buildActiveQuestionIds(activeId)
		r.sadd(key, ids)

	def getInfo(self, id):
		r = redis.StrictRedis(connection_pool = POOL)
		if(r):
			key = self._buildInfoKey(id)
			cacheValue = r.get(key)
			if(cacheValue is not None):
				result = json.loads(cacheValue)
				return result
		result = self._dao.queryInfo(id)
		if result is not None and r is not None:
			self._initInfo(r, key, result)

		return result.__dict__

	###检查答案
	def checkAnswer(self, questionId, answerId):
		r = redis.StrictRedis(connection_pool = POOL)
		key = self._buildInfoKey(questionId)
		if(r):
			cacheValue = r.get(key)
			if(cacheValue is not None):
				result = json.loads(cacheValue)
				return int(answerId) == int(result['rightAnswerId'])
		result = self._dao.queryInfo(questionId)
		if(result is None):
			return False
		self._initInfo(r, key, result)
		return int(answerId) == int(result.rightAnswerId)

	def _initInfo(self, r, key, result):
		r.set(key, json.dumps(result.__dict__))

	def _buildInfoKey(self, id):
		return info_key + str(id)

	def _buildActiveQuestionIds(self, activeId):
		return ACTIVEID_QUESTIONID_SET_PREFIX_KEY + str(activeId)
