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

from h5game_backend import LOGGER
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
		gameActiveInfo = self._gameActiveInfoService.getInfoBySignWord(signWord)
		
		if not gameActiveInfo:
			return None

		gameActivePrizeInfos = self._gameActivePrizeInfoService.getInfosByActiveId(gameActiveInfo['id'])

		return {"info": gameActiveInfo, "prizes": gameActivePrizeInfos}

	def gamePlayInfo(self, signWord, step):
		gameActiveInfo = self._gameActiveInfoService.getInfoBySignWord(signWord)
		if not gameActiveInfo:
			return None

	def sharePlay(self, userId, activeId, shareCode):
		##用户权限检测
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		if activeInfo is None:
			return {'success': False, "failedType": "illegal"}
		###是否中奖了		
		prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeId)
		if prizeInfo:
			return self._handlePrized(activeInfo, prizeInfo)
		###shareCode有效性检测
		shareActiveId = self._userShareInfoService.getShareActiveId(shareCode)
		if shareActiveId is None or int(shareActiveId) != int(activeId):
			return {'success': False, 'failedType': 'illegal'}
		####检查用户能玩的共享过来的游戏总数
		count = self._userPlayShareGameInfoService.countUserPlay(userId, activeId)
		if count > BizStatusUtils.MAX_SHARED_PLAY:
			return {'success': False, 'failedType': 'limit'}
		sharePlayInfo = self._userPlayShareGameInfoService.getUserPlayInfo(userId, activeId, shareCode)
		if sharedPrePlayInfo is not None:
			if sharedPrePlayInfo['result'] == BizStatusUtils.PLAY_RESULT_INIT:
				return self._continuePlay(sharedPrePlayInfo)
			elif sharedPrePlayInfo['result'] == BizStatusUtils.PLAY_RESULT_SUCCESS:
				return self._gotoRecivePrize(userId, activeId)
			else:
				return {'success': False, 'failedType': 'limit'}
		####用户分享的且没有玩
		firstQuestion, randomQuestionIds = self._gameQuestionInfoService.randomAndGetUserFirstQuestion(activeId)
		#def addUserPlayInfo(self, userId, activeId, shareCode, randomQuestionIds, playQuestionId):
		playInfo = self._userPlayShareGameInfoService.addUserPlayInfo(userId, activeId, shareCode, randomQuestionIds, firstQuestion['id'])
		if playInfo:
			return self._continuePlay(playInfo, firstQuestion)
		return {'success': False, 'failedType': 'server'}
##第一步条案，无须检查答案是否正确
		# if(step == 1):
		# 	self._gameQuestionInfoService.
		return None

	def firstPlay(self, userId, activeId):
		##用户权限检测
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		if activeInfo is None:
			return {'success': False, "failedType": "illegal"}
		###是否中奖了		
		prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeId)
		if prizeInfo:
			return self._handlePrized(activeInfo, prizeInfo)

		##用户上一次玩结束了吗
		playInfo = self._userPlayOriginGameInfoService.getInfo(userId, activeId)
		if playInfo is None:
			return self._playOriginGame(userId, activeId)
		####查看用户玩分享过来的链接的情况
		sharedPrePlayInfo = self._userPlayShareGameInfoService.getUserlastPlayInfo(userId, activeId)
		if sharedPrePlayInfo is not None and sharedPrePlayInfo['result'] == 0:
			return self._continuePlay(sharedPrePlayInfo)
		######用户有正在玩的记录
		###return self._play
		return self._handlePrePlay(playInfo)

####处理用户玩过了的情况 系统给的游戏次数#####
	def _handlePrePlay(self, playInfo):
		###要给我得奖的啊
		if int(playInfo['result']) == BizStatusUtils.PLAY_RESULT_SUCCESS:
			return self._gotoRecivePrize(playInfo['userId'], playInfo['activeId'])
		####用户还能再玩,要么继续，要么在以前错误的上面继续
		if playInfo['result'] == BizStatusUtils.PLAY_RESULT_INIT or playInfo['failedCount'] < BizStatusUtils.MAX_FAILED_NUMBER:
			return self._continuePlay(playInfo)
		#####已达到个人最大可玩数,需要根据分享的情况来决定如何
		if playInfo['failedCount'] == BizStatusUtils.MAX_SELF_PLAY:
			return self._sharedToPlay(playInfo['userId'], playInfo['activeId'])
		####用户最大个人可玩数已玩了，查看是否有未玩完的共享游戏
		if playInfo['failedCount'] >= MAX_ORIGIN_PLAY:
			return {'success': False, 'failedType': 'limit'}

	def _playOriginGame(self, userId, activeId):###用户还能再玩
		firstQuestion, randomQuestionIds = self._gameQuestionInfoService.randomAndGetUserFirstQuestion(activeId)
		playInfo = self._userPlayOriginGameInfoService.addUserPlayInfo(userId, activeId, randomQuestionIds, firstQuestion['id'])
		if playInfo:
			return self._continuePlay(playInfo, firstQuestion)
		return {'success': False, 'failedType': 'server'}

	######如果用户未分享过，则弹出叫用户分享，否则，无法继续游戏，告诉用户
	def _sharedToPlay(self, userId, activeId):
		shared = self._userShareInfoService.userShared(userId, activeId)
		if not shared:
			##获取用户分享的链接
			openId = self._userInfoService.getUserOpenId(userId)
			if openId is None:
				return {'success': False, 'failedType': 'illegal'}
			shareInfo = self._userShareInfoService.genShareInfo(userId, openId, activeId, activeInfo['url'])
			if shareInfo is None:
				return {'success': False, 'failedType': 'illegal'}
			else:
				return {'success': True, 'needShare': True, 'shareInfo': shareInfo}
		return {'success': False, 'failedType': 'shared'}
	
	#####开始在接口层面区分来自于共享的还是系统提供的游戏机会,此接口只供系统提供的游戏机会中调用
	#####resp=  {'sucess': True/False, 'failedType': 'illegal'|'server'|'limit', 'play':True, \
	############'needShare': True, 'prized', 'activeInfo': activeInfo, 'playInfo': playInfo,  \
	############'prizeInfo': prizeInfo, 'question': question, "answers": answers}
	def next(self, userId, activeId, questionId, answerId):
		playInfo = self._userPlayOriginGameInfoService.getInfo(activeId, questionId)
		###用户请求有问题
		if playInfo is None or playInfo['playQuestionId'] != questionId:
			return {'success': False, 'failedType': 'illegal'}

		rightAnswer = self._gameQuestionInfoService.checkAnswer(questionId, answerId)
		if rightAnswer:
			return self._gotoNext(self, userId, activeId, questionId, playInfo)
		else:
			self._userPlayOriginGameInfoService.modifyResultFailedCount(playInfo['id'], BizStatusUtils.PLAY_RESULT_FAILED, 1)			
			playInfo = self._userPlayOriginGameInfoService.getLastPlay(activeId, questionId)
			return self._handlePrePlay(playInfo)
	
	###在答题成功后，下一个题目
	def _gotoNext(self, userId, activeId, preQuestionId, playInfo):
		questionIds =playInfo['questionIds']
		preIndex = -1
		for index, value in enumerate(questionIds):
			if int(value) == int(preQuestionId):
				preIndex = index
				break
		if preIndex == -1:
			return {'success': False, 'failedType': 'illegal'}
		###问题答完了
		###获取抽奖码
		if preIndex == len(questionIds) - 1:
			self._userPlayOriginGameInfoService.modifyResult(playInfo['id'], BizStatusUtils.PLAY_RESULT_SUCCESS)
			return self._gotoRecivePrize(userId, activeId)
		#####下一个问题
		questionId = questionIds[preIndex + 1]
		question = self._gameQuestionInfoService.getInfo(questionId)		
		if question is None:
			return None
		self._userPlayOriginGameInfoService.modifyPlayQuestionId(playInfo['id'], questionId)
		playInfo = self._userPlayOriginGameInfoService.getInfo(userId, activeId)
		return self._continuePlay(playInfo, question)

	###用户领奖给用户生成抽奖码，并返回
	def _gotoRecivePrize(self, userid, activeId):
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		prizeInfo = self._userPrizedInfoService.genPrize(userId, activeId)
		if activeInfo is None or prizeInfo is None:
			return {'success': False, 'failedType': 'illegal'}
		return self._handlePrized(activeInfo, prizeInfo)


	def _handlePrized(self, activeInfo, prizeInfo):
		return {'success': True, 'prized': True, 'activeInfo': activeInfo, 'prizeInfo': prizeInfo}

	def _initReturnQuestion(self, question, playInfo):
		if question is None:
			return {'success': False, 'failedType': 'illegal'}
		if playInfo is None:
			return {'success': False, 'failedType': 'illegal'}			
 		originGame = 'sharedCode' in playInfo
		answers = self._initQuestionPossibleAnswerInfo(question);
		if answers is None or not answers:
			return {'success': False, 'failedType': 'illegal'}
		return {'success': True, 'play': True, 'originGame': originGame, 'question': question, 'answers': answers}

	################originGame是否原生游戏#############
	def _continuePlay(self, playInfo, question = None):
		if question is None:
			questionId = playInfo['playQuestionId']
			question = self._gameQuestionInfoService.getInfo(questionId)
		return self._initReturnQuestion(question, playInfo)

	def _initQuestionPossibleAnswerInfo(self, question):
		if question is None:
			return {'success': False, 'failedType': 'illegal'}
		answerIdsStr = question['possibleAnswerIds']
		answerIds = answerIdsStr.split(",")
		answerIdList = []
		for answerId in answerIds:
			answerId = answerId.strip()
			answerIdList.append(answerId)
		return self._gameAnswerInfoService.getInfos(answerIdList)

	def _userId(self, openId):
		return self._userInfoService.getUserId(openId)


	####答错题目了，检查用户还能再玩么？不能再玩，就需要查看分享了，要是也不能分享，则告诉用户没得玩了，只能玩朋友的
	# def _handleAnswerQuestionFailed(self, userId, activeId, questionId):
	# 	####has more self play
	# 	playCount = self._userPrizedInfoService.count(userId, activeId)
	# 	if(playCount >= MAX_ORIGIN_PLAY):
	# 		return {'play': False}
	# 	if(playCount == MAX_SELF_PLAY):
	# 		###用户上一次玩结束了吗
	# 		###需要分享才能玩
	# 		###用户是否已经分享
	# 		shared = self._userShareInfoService.userShared(userId, activeId)
	# 		if not shared:
	# 			##获取用户分享的链接
	# 			openId = self._userInfoService.getUserOpenId(userId)
	# 			if openId is None:
	# 				return None
	# 			shareInfo = self._userShareInfoService.genShareInfo(userId, openId, activeId, activeInfo['url'])
	# 			if shareInfo is None:
	# 				return None
	# 			else:
	# 				return {'needShare': True, 'shareInfo': shareInfo}

		

