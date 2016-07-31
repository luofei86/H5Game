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

#####主业务类


MAX_SELF_PLAY=2
MAX_ORIGIN_PLAY=3
MAX_SHARED_PLAY=20

PLAY_RESULT_SUCCESS = 1;
PLAY_RESULT_FAILED = -1;
PLAY_RESULT_INIT = 0;

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
			return {'success': False, "failedType": "illegal"}
		##用户权限检测
		prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeId)
		if prizeInfo:
			return {'success': True, 'prized': True, 'prizeInfo': prizeInfo, 'activeInfo': activeInfo}

		##用户上一次玩结束了吗
		playInfo = self._userPlayOriginGameInfoService.getInfo(userId, activeId)
		if playInfo is None:
			return self._playOriginGame(userId, activeId)

		if playInfo['result'] == PLAY_RESULT_SUCCESS:###要给我得奖的啊
			return self._playPrized(userId, activeId, playInfo)
		####用户还能再玩,要么继续，要么在以前错误的上面继续
		if playInfo['result'] == PLAY_RESULT_INIT || playInfo['failedCount'] == 1:
			return self._playPreOriginGame(userId, activeId, playInfo)

		if playInfo['failedCount'] == MAX_ORIGIN_PLAY:
			return self._sharedToPlay(userId, activeId)

		if playInfo is not None and playInfo['failedCount'] >= MAX_ORIGIN_PLAY:
			return self._playSharedGame(userId, activeId)

	def _playOriginGame(self, userId, activeId):###用户还能再玩
		firstQuestion, randomQuestionIds = self._gameQuestionInfoService.randomAndGetUserFirstQuestion(activeId)
		addResult = self._userPlayOriginGameInfoService.addUserPlayInfo(userId, activeId, randomQuestionIds, firstQuestion['id'])
		if addResult:
			return self._initReturnQuestion(firstQuestion)
		return None
	def _playPreOriginGame(self, userId, activeId, playInfo):
		

	###查看是否有未完成的共享游戏
	def _playSharedGame(self, userId, activeId):


	def _initReturnQuestion(self, question):		
		answerIdsStr = question['possibleAnswerIds']
		answerIds = answerIdsStr.split(",")
		answerIdList = []
		for answerId in answerIds:
			answerId = answerId.strip()
			answerIdList.append(answerId)
		answers = self._gameAnswerInfoService.getInfos(answerIdList)

		return {'success': True, 'play': True, 'question': firstQuestion, "answers": answers}

	def next(self, userId, activeId, questionId, answerId):
		playInfo = self._userPlayOriginGameInfoService.getLastPlay(activeId, questionId)
		###用户请求有问题
		if playInfo is None or playInfo['playQuestionId'] != questionId:
			return None

		rightAnswer = self._gameQuestionInfoService.checkAnswer(questionId, answerId)
		if rightAnswer:
			return self._gotoNext(self, userId, activeId, questionId, playInfo)
		else:
			self._userPlayOriginGameInfoService.modifyResult(playInfo['id'], PLAY_RESULT_FAILED)
			return self._handleAnswerQuestionFailed(userId, activeId, questionId, playInfo)

	####答错题目了，检查用户还能再玩么？不能再玩，就需要查看分享了，要是也不能分享，则告诉用户没得玩了，只能玩朋友的
	####
	def _handleAnswerQuestionFailed(self, userId, activeId, questionId):
		####has more self play
		playCount = self._userPrizedInfoService.count(userId, activeId)
		if(playCount >= MAX_ORIGIN_PLAY):
			return {'play': False}
		if(playCount == MAX_SELF_PLAY):
			###用户上一次玩结束了吗
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




	def _sharedToPlay(self, userId, activeId):
	###用户上一次玩结束了吗
		###需要分享才能玩
		###用户是否已经分享
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
		
###在答题成功后，下一个题目
	def _gotoNext(self, userId, activeId, preQuestionId, playInfo):
		questionIds =playInfo['questionIds']
		preIndex = -1
		for index, value in enumerate(questionIds):
			if int(value) == (int) preQuestionId:
				preIndex = index
				break
		if preIndex == -1:
			return None
		###获取抽奖码
		if preIndex == len(questionIds) - 1:
			self._userPlayOriginGameInfoService.modifyResult(playInfo['id'], PLAY_RESULT_SUCCESS)
			return self._userGetThePrize(userId, activeId)
		questionId = questionIds[preIndex + 1]
		question = self._gameQuestionInfoService.getInfo(questionId)		
		if question is None:
			return None
		self._userPlayOriginGameInfoService.modifyPlayQuestionId(playInfo['id'], questionId)
		return self._initReturnQuestion(question)

#########
#	def share(self, openId, activeId, shareCode):

	def _handlePrePlayShared(self, playInfo):
		questionId = playInfo['playQuestionId']
		question = self._gameQuestionInfoService.getInfo(questionId)
		if question is None:
			return None			
		answers = self._initQuestionPossibleAnswerInfo(question);
		if answers is None or not answers:
			return None
		return {'play': True, 'question': questionId, 'answers': answers}

	def _handlePrePlayOrigin(self, playInfo):
		questionId = playInfo['playQuestionId']
		question = self._gameQuestionInfoService.getInfo(questionId)
		if question is None:
			return None			
		answers = self._initQuestionPossibleAnswerInfo(question);
		if answers is None or not answers:
			return None
		return {'play': True, 'question': question, 'answers': answers}


	def _initQuestionPossibleAnswerInfo(self, question):
		if question is None:
			return None
		answerIdsStr = question['possibleAnswerIds']
		answerIds = answerIdsStr.split(",")
		answerIdList = []
		for answerId in answerIds:
			answerId = answerId.strip()
			answerIdList.append(answerId)
		return self._gameAnswerInfoService.getInfos(answerIdList)

	def _userId(self, openId):
		return self._userInfoService.getUserId(openId)


		

