# -*- coding: utf-8 -*-

import urllib

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


from h5game_backend import LOGGER
from h5game_backend import app
from models import BizStatusUtils

#####主业务类

class GameBizService:
	def __init__(self):
		#LOGGER.info("Init 1")
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
		activeInfo = self._gameActiveInfoService.getInfoBySignWord(signWord)		
		if not activeInfo:
			return None
		prizes = self._gameActivePrizeInfoService.getInfosByActiveId(activeInfo['id'])
		###check user prized
		###是否中奖了
		prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeInfo['id'])

		if prizeInfo:
			LOGGER.debug("User prized info:" + str(prizeInfo))
			return self._handlePrized(activeInfo, prizeInfo)
		LOGGER.info("Goto homepage.")
		return {'success': True, 'welcome': True, 'activeInfo': activeInfo, 'prizes': prizes}

#self.gameBizService.afterShared(userId, shareCode, activeId)
	def afterShared(self, userId, shareCode, activeId):
		self._userShareInfoService.modifyResult(userId, shareCode, activeId, BizStatusUtils.SHARED_SUCCESS)

	def _handleIllegalResp(self, failedType = 'illegal', message="data access failed"):
		return {'success': False, 'failedType': failedType, 'message': message}
#######
	def playShareGame(self, userId, openId, activeId, shareCode):
		##用户权限检测
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		if activeInfo is None:
			return self._handleIllegalResp(message="no activeInfo info:" + activeId)
		###是否中奖了
		activeId = activeInfo['id']
		prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeId)
		if prizeInfo:
			return self._handlePrized(activeInfo, prizeInfo)
		###shareCode有效性检测
		shareInfo = self._userShareInfoService.getInfoByShareCode(shareCode)
		if shareInfo is None or int(shareInfo['activeId']) != int(activeId):
			return self._handleIllegalResp(message="illegal info failed.")

		sharePlayInfo = self._userPlayShareGameInfoService.getInfo(userId, activeId, shareCode)
		if sharePlayInfo is not None:
			playInfoResult = int(sharePlayInfo['result'])
			if playInfoResult == BizStatusUtils.PLAY_RESULT_SUCCESS:
				return self._gotoRecivePrize(userId, activeId)
			else:
				return self._continuePlay(sharePlayInfo, activeInfo = activeInfo)
		firstQuestion, randomQuestionIds = self._gameQuestionInfoService.randomAndGetUserFirstQuestion(activeId)
		#def addUserPlayInfo(self, userId, activeId, shareCode, randomQuestionIds, playQuestionId):
		playInfo = self._userPlayShareGameInfoService.addUserPlayInfo(userId, activeId, shareCode, randomQuestionIds, firstQuestion['id'])
		if playInfo:
			return self._continuePlay(playInfo, firstQuestion, activeInfo = activeInfo)
		return self._handleIllegalResp(failedType="server")

	def playGame(self, userId, activeId):
		##用户权限检测
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		if activeInfo is None:
			LOGGER.debug("No active info")
			return self._handleIllegalResp()
		###是否中奖了		
		prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeId)
		if prizeInfo:
			LOGGER.debug("No prize info")
			return self._handlePrized(activeInfo, prizeInfo)

		##用户上一次玩结束了吗
		playInfo = self._userPlayOriginGameInfoService.getInfo(userId, activeId)
		if playInfo is None:
			LOGGER.debug("No playInfo info go to play origin game")
			return self._playOriginGame(userId, activeId)
		######用户有正在玩的记录
		return self._continuePlay(playInfo)

	def _playOriginGame(self, userId, activeId):###用户还能再玩
		firstQuestion, randomQuestionIds = self._gameQuestionInfoService.randomAndGetUserFirstQuestion(activeId)
		LOGGER.debug("First question:" + str(firstQuestion))
		# LOGGER.debug("Random question ids:" + randomQuestionIds)
		playInfo = self._userPlayOriginGameInfoService.addUserPlayInfo(userId, activeId, randomQuestionIds, firstQuestion['id'])		
		if playInfo:
			return self._continuePlay(playInfo, firstQuestion)
		return self._handleIllegalResp(failedType="server")

	#####开始在接口层面区分来自于共享的还是系统提供的游戏机会,此接口只供系统提供的游戏机会中调用
	#####resp=  {'sucess': True/False, 'failedType': 'illegal'|'server'|'limit', 'play':True, \
	############'needShare': True, 'prized', 'activeInfo': activeInfo, 'playInfo': playInfo,  \
	############'prizeInfo': prizeInfo, 'question': question, "answers": answers}
	def originGameNext(self, userId, activeId, questionId, answerId):
		playInfo = self._userPlayOriginGameInfoService.getInfo(userId, activeId)
		if playInfo is None:
			return self._handleIllegalResp()

		if int(playInfo['playQuestionId']) != int(questionId):
			###用户当前玩的问题和数据库数据不对，可能是微信客户端里点后退了
			prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeId)
			if prizeInfo:
				activeInfo = self._gameActiveInfoService.getInfo(activeId)
				return self._handlePrized(activeInfo, prizeInfo)
			return self._continuePlay(playInfo)
		rightAnswer = self._gameQuestionInfoService.checkAnswer(questionId, answerId)
		if rightAnswer:
			return self._gotoNext(userId, activeId, questionId, playInfo)
		else:
			resp =  self._continuePlay(playInfo)
			resp['answerFailed'] = True
			return resp

	def shareGameNext(self, userId, activeId, shareCode, questionId, answerId):
		playInfo = self._userPlayShareGameInfoService.getInfo(userId, activeId, shareCode)
		if playInfo is None:
			return self._handleIllegalResp(message="No playInfo or the question id is wrong.")

		###用户当前玩的问题和数据库数据不对，可能是微信客户端里点后退了
		if int(playInfo['playQuestionId']) != int(questionId):
			prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeId)
			if prizeInfo:
				activeInfo = self._gameActiveInfoService.getInfo(activeId)
				return self._handlePrized(activeInfo, prizeInfo)
			return self._continuePlay(playInfo)
		rightAnswer = self._gameQuestionInfoService.checkAnswer(questionId, answerId)
		if rightAnswer:
			return self._gotoSharedGameNext(userId, activeId, shareCode, questionId, playInfo)
		else:
			resp = self._continuePlay(playInfo)
			resp['answerFailed'] = True
			return resp

	def _initQuestionIds(self, questionIdsStr):
		questionIds = questionIdsStr.split(",")
		questionIdList = []
		for questionId in questionIds:
			questionId = questionId.strip()
			questionIdList.append(questionId)
		return questionIdList
	
	###在答题成功后，下一个题目
	def _gotoNext(self, userId, activeId, preQuestionId, playInfo):
		questionIdsStr = playInfo['questionIds']
		questionIdList = self._initQuestionIds(questionIdsStr)
		preIndex = -1
		for index, value in enumerate(questionIdList):
			if int(value) == int(preQuestionId):
				preIndex = index
				break
		if preIndex == -1:
			return self._handleIllegalResp()
		###问题答完了
		###获取抽奖码
		if preIndex == len(questionIdList) - 1:
			self._userPlayOriginGameInfoService.modifyResult(playInfo['id'], userId, activeId, BizStatusUtils.PLAY_RESULT_SUCCESS)
			return self._gotoRecivePrize(userId, activeId)
		#####下一个问题
		questionId = questionIdList[preIndex + 1]
		question = self._gameQuestionInfoService.getInfo(questionId)		
		if question is None:
			return self._handleIllegalResp()
		self._userPlayOriginGameInfoService.modifyPlayQuestionId(playInfo['id'], userId, activeId, questionId)
		playInfo = self._userPlayOriginGameInfoService.getInfo(userId, activeId)
		return self._continuePlay(playInfo, question)

	###在答题成功后，下一个题目
	def _gotoSharedGameNext(self, userId, activeId, shareCode, preQuestionId, playInfo):
		questionIdsStr = playInfo['questionIds']
		questionIdList = self._initQuestionIds(questionIdsStr)
		preIndex = -1
		for index, value in enumerate(questionIdList):
			if int(value) == int(preQuestionId):
				preIndex = index
				break
		if preIndex == -1:
			return self._handleIllegalResp()
		###问题答完了
		###获取抽奖码
		if preIndex == len(questionIdList) - 1:
			self._userPlayShareGameInfoService.modifyResult(playInfo['id'], userId, activeId, shareCode, BizStatusUtils.PLAY_RESULT_SUCCESS)
			return self._gotoRecivePrize(userId, activeId)
		#####下一个问题
		questionId = questionIdList[preIndex + 1]
		question = self._gameQuestionInfoService.getInfo(questionId)		
		if question is None:
			return self._handleIllegalResp()
		self._userPlayShareGameInfoService.modifyPlayQuestionId(playInfo['id'], userId, activeId, shareCode, questionId)
		playInfo = self._userPlayShareGameInfoService.getInfo(userId, activeId, shareCode)
		return self._continuePlay(playInfo, question)


	###用户领奖给用户生成抽奖码，并返回
	def _gotoRecivePrize(self, userId, activeId):
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		prizeInfo = self._userPrizedInfoService.genPrize(userId, activeId)
		if activeInfo is None or prizeInfo is None:
			return self._handleIllegalResp()
		return self._handlePrized(activeInfo, prizeInfo)

	def _handlePrized(self, activeInfo, prizeInfo):
		return {'success': True, 'prized': True, 'activeInfo': activeInfo, 'prizeInfo': prizeInfo}

	def _initReturnQuestion(self, question, playInfo, activeInfo):
		if question is None or playInfo is None or activeInfo is None:
			return self._handleIllegalResp()
 		
		answers = self._initQuestionPossibleAnswerInfo(question)
		if answers is None or not answers:
			return self._handleIllegalResp()

		questionIdsStr = playInfo['questionIds']
		questionIdList = self._initQuestionIds(questionIdsStr)
		numberIndex = -1

		for i_id in questionIdList:
			numberIndex = numberIndex + 1
			if str(i_id) == str(question['id']):
				break
		if 'shareCode' in playInfo:
			return {'success': True, 'play': True, 'activeInfo': activeInfo, 'playInfo': playInfo, 'question': question, 'answers': answers, 'numberIndex': numberIndex, 'shareCode': playInfo['shareCode']}
		else:
			return {'success': True, 'play': True, 'activeInfo': activeInfo, 'playInfo': playInfo, 'question': question, 'answers': answers, 'numberIndex': numberIndex}

	################originGame是否原生游戏#############
	def _continuePlay(self, playInfo, question = None, activeInfo = None):
		if question is None:
			questionId = playInfo['playQuestionId']
			question = self._gameQuestionInfoService.getInfo(questionId)
		if activeInfo is None:
			activeInfo = self._gameActiveInfoService.getInfo(playInfo['activeId'])
		return self._initReturnQuestion(question, playInfo, activeInfo)

	def _initQuestionPossibleAnswerInfo(self, question):
		if question is None:
			return self._handleIllegalResp()
		answerIdsStr = question['possibleAnswerIds']
		answerIds = answerIdsStr.split(",")
		answerIdList = []
		for answerId in answerIds:
			answerId = answerId.strip()
			answerIdList.append(answerId)
		return self._gameAnswerInfoService.getInfos(answerIdList)

	def _userId(self, openId):
		return self._userInfoService.getUserId(openId)

	def genUserShareContent(self, userId, openId, activeId, appId, signWord):
		shareInfo = self._userShareInfoService.getInfoByUserIdActiveId(userId, activeId)
		if shareInfo:			
			return shareInfo
		shareCode = self._userShareInfoService.buildShareCode(openId)
		shareUrl = self._getShareUrl(signWord, shareCode)

		##def genShareInfo(self, userId, openId, activeId, shareCode, shareUrl):
		return self._userShareInfoService.genShareInfo(userId, openId, activeId, shareCode, shareUrl)


	def _getShareUrl(self, signWord, shareCode):
		return "http://h5.yiketalks.com/game/redirect/" + signWord + "/" + shareCode

