# -*- coding: utf-8 -*-

from services import GameActiveInfoService
from services import GameQuestionInfoService
from services import GameActivePrizeInfoService
from services import GameAnswerInfoService

from services import UserInfoService
from services import UserPlayOriginGameInfoService
from services import UserPlayShareGameInfoService
from services import UserShareInfoService
from services import UserShareLimitInfoService
from services import UserPrizeInfoService

#####主业务类


MAX_SELF_PLAY=2
MAX_ORIGIN_PLAY=3
MAX_SHARED_PLAY=20


class GameBizService:
	def __init__(self):
		self._gameActiveInfoService = GameActiveInfoService.GameActiveInfoService()
		self._gameQuestionInfoService = GameQuestionInfoService.GameQuestionInfoService()
		self._gameActivePrizeInfoService = GameActivePrizeInfoService.GameActivePrizeInfoService()
		self._gameAnswerInfoService = GameAnswerInfoService.GameAnswerInfoService()

		self._userPrizedInfoService = UserPrizeInfoService.UserPrizeInfoService()
		self._userPlayOriginGameInfoService = UserPlayOriginGameInfoService.UserPlayOriginGameInfoService()
		self._userPlayShareGameInfoService = UserPlayShareGameInfoService.UserPlayShareGameInfoService()
		self._userShareInfoService = UserShareInfoService.UserShareInfoService()
		self._userShareLimitInfoService = UserShareLimitInfoService.UserShareLimitInfoService()
		self._userInfoService = UserInfoService.UserInfoService()


#####获取此Url或signWord对应的activeId
	def gameHomepageInfo(self, userId, signWord):
		gameActiveInfo = self._gameActiveInfoService.getInfoBySignWord(signWord)
		
		if not gameActiveInfo:
			return None

		gameActivePrizeInfos = self._gameActivePrizeInfoService.getInfosByActiveId(gameActiveInfo['id'])

		return {"info": gameActiveInfo, "prizes": gameActivePrizeInfos}

	def gamePlayInfo(self, signWord, step):
		gameActiveInfo = self._gameActiveInfoService.getInfoBySignWord(signWord)

		if not gameActiveInfo:
			return None
##第一步条案，无须检查答案是否正确
		# if(step == 1):
		# 	self._gameQuestionInfoService.
		return None

	def firstPlay(self, userId, activeId):
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		if activeInfo is None:
			return None
		##用户权限检测
		prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeId)
		if prizeInfo:
			###用户有抽奖码了
			if activeId:
				return {'prized': True, 'prizeInfo': prizeInfo, 'activeInfo': activeInfo}
			else:
				return None
		##用户没中奖,用户还能玩吗
		playCount = self._userPlayOriginGameInfoService.countUserPlay(userId, activeId)
		####用户原生能玩的都玩完了
		if(playCount >= MAX_ORIGIN_PLAY):
			return {'play': False}
		if(playCount == MAX_SELF_PLAY):
			###需要分享才能玩
			###用户是否已经分享
			shared = self._userShareInfoService.userShared(userId, activeId)
			if not shared:
				##获取用户分享的链接
				openId = self._userInfoService.getUserOpenId(userId)
				if openId is None:
					return None
				shareInfo = self._userShareInfoService.genShareInfo(userId, openId, activeId, activeInfo['url'])
				if shareInfo is None:
					return None
				else:
					return {'needShare': True, 'shareInfo': shareInfo}
		###用户还能再玩
		firstQuestion, randomQuestionIds = self._gameQuestionInfoService.randomAndGetUserFirstQuestion(activeId)
		self._userPlayOriginGameInfoService.addUserPlayInfo(userId, activeId, randomQuestionIds, firstQuestion['id'])
		print firstQuestion
		answerIdsStr = firstQuestion['possibleAnswerIds']
		answerIds = answerIdsStr.split(",")
		answerIdList = []
		for answerId in answerIds:
			answerId = answerId.strip()
			answerIdList.append(answerId)
		answers = self._gameAnswerInfoService.getInfos(answerIdList)

		return {'play': True, 'question': firstQuestion, "answers": answers}

#########
#	def share(self, openId, activeId, shareCode):


	def _userId(self, openId):
		return self._userInfoService.getUserId(openId)


		

