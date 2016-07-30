# -*- coding: utf-8 -*-

from services import GameActiveInfoService
from services import GameQuestionInfoService
from services import UserShareInfoService
from services import UserShareLimitInfoService
from services import GameActivePrizeInfoService

#####主业务类


class GameBizService:
	def __init__(self):
		self._gameActiveInfoService = GameActiveInfoService.GameActiveInfoService()
		self._gameQuestionInfoService = GameQuestionInfoService.GameQuestionInfoService()
		self._userShareInfoService = UserShareInfoService.UserShareInfoService()
		self._userShareLimitInfoService = UserShareLimitInfoService.UserShareLimitInfoService()
		self._gameActivePrizeInfoService = GameActivePrizeInfoService.GameActivePrizeInfoService()

#####获取此Url或signWord对应的activeId
	def gameHomepageInfo(self, userId, signWord):
		gameActiveInfo = self._gameActiveInfoService.getInfoBySignWord(signWord)
		print gameActiveInfo
		if not gameActiveInfo:
			return None

		gameActivePrizeInfos = self._gameActivePrizeInfoService.getInfosByActiveId(gameActiveInfo['id'])

		return {"info": gameActiveInfo, "prizes": gameActivePrizeInfos}