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
from services import WeixinService


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
		self._weixinService = WeixinService.WeixinService(app.config.get('APP_ID', None), app.config.get('APP_SECERT', None))


#####获取此Url或signWord对应的activeId
	def gameHomepageInfo(self, userId, signWord):
		activeInfo = self._gameActiveInfoService.getInfoBySignWord(signWord)		
		if not activeInfo:
			return None
		prizes = self._gameActivePrizeInfoService.getInfosByActiveId(activeInfo['id'])
		###check user prized
		###是否中奖了
		LOGGER.debug(str(userId))
		LOGGER.debug(activeInfo['id'])
		prizeInfo = self._userPrizedInfoService.getUserPrizeInfo(userId, activeInfo['id'])

		if prizeInfo:
			return self._handlePrized(activeInfo, prizeInfo)
		return {'success': True, 'welcome': True, 'activeInfo': activeInfo, 'prizes': prizes}

	def _handelNoMoreCanPlayResp(self, activeId):
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		prizes = self._gameActivePrizeInfoService.getInfosByActiveId(activeInfo['id'])
		return {'success': False, "activeInfo": activeInfo, 'failedType': 'limit', 'prizes': prizes}

	def userShared(self, id, shareCode):
		userShareInfo = self._userShareInfoService.getInfo(id)
		if userShareInfo is None or userShareInfo['shareCode'] != shareCode:
			return self._handleIllegalResp()		
		###已经分享过了，则处理下是否能继续玩的问题，即用户失败次数是否大于3
		if int(userShareInfo['result']) == BizStatusUtils.SHARED_SUCCESS:
			playInfo = self._userPlayOriginGameInfoService.getInfo(userShareInfo['userId'], userShareInfo['activeId'])
			if playInfo is None:
				return self._handleIllegalResp()
			if int(playInfo['failedCount']) <= BizStatusUtils.MAX_SELF_PLAY:
				return self._continuePlay(playInfo)
			else:
				return self._handelNoMoreCanPlayResp(userShareInfo['activeId'])

		self._userShareInfoService.modifyResult(id, BizStatusUtils.SHARED_SUCCESS)
		###共享成功了，修改
		playInfo = self._userPlayOriginGameInfoService.getInfo(userShareInfo['userId'], userShareInfo['activeId'])
		if playInfo is None:
			return self._handleIllegalResp()
		return self._continuePlay(playInfo)

	def _handleIllegalResp(failedType = 'illegal', message="data access failed"):
		return {'success': False, 'failedType': failedType, 'message': message}
#######
	def playShareGame(self, userId, unionId, activeId, shareCode):
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
		 # \
			# or int(shareInfo['result']) != BizStatusUtils.SHARED_SUCCESS \
			# or int(shareInfo['userId']) == userId:
			return self._handleIllegalResp(message="illegal info failed.")

		####检查用户能玩的共享过来的游戏总数
		count = self._userPlayShareGameInfoService.countUserPlay(userId, activeId)
		if int(count) > BizStatusUtils.MAX_SHARED_PLAY:
			return self._handelNoMoreCanPlayResp(activeId)
		sharePlayInfo = self._userPlayShareGameInfoService.getInfo(userId, activeId, shareCode)
		if sharePlayInfo is not None:
			playInfoResult = int(sharePlayInfo['result'])
			if playInfoResult == BizStatusUtils.PLAY_RESULT_INIT:
				return self._continuePlay(sharePlayInfo, activeInfo = activeInfo)
			elif playInfoResult == BizStatusUtils.PLAY_RESULT_SUCCESS:
				return self._gotoRecivePrize(userId, activeId)
			else:
				return self._handelNoMoreCanPlayResp(activeId)
		####用户分享的且没有玩
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
			return self._handleIllegalResp()
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
		if sharedPrePlayInfo is not None and int(sharedPrePlayInfo['result']) == 0:
			return self._continuePlay(sharedPrePlayInfo, activeInfo = activeInfo)
		######用户有正在玩的记录
		###return self._play
		return self._handlePrePlay(playInfo)

####处理用户玩过了的情况 系统给的游戏次数#####
	def _handlePrePlay(self, playInfo):
		###要给我得奖的啊
		if int(playInfo.get('result')) == BizStatusUtils.PLAY_RESULT_SUCCESS:
			return self._gotoRecivePrize(playInfo['userId'], playInfo['activeId'])
		####用户还能再玩,要么继续，要么在以前错误的上面继续
		if int(playInfo.get('result')) == BizStatusUtils.PLAY_RESULT_INIT or int(playInfo['failedCount']) < BizStatusUtils.MAX_FAILED_NUMBER:
			return self._continuePlay(playInfo)
		#####已达到个人最大可玩数,需要根据分享的情况来决定如何
		if int(playInfo.get('failedCount')) == BizStatusUtils.MAX_SELF_PLAY:
			LOGGER.debug("Failed to shared.")
			return self._sharedToPlay(playInfo)
		####用户最大个人可玩数已玩了，查看是否有未玩完的共享游戏
		if int(playInfo.get('failedCount')) >= BizStatusUtils.MAX_ORIGIN_PLAY:
			return self._handelNoMoreCanPlayResp(playInfo['activeId'])

	def _playOriginGame(self, userId, activeId):###用户还能再玩
		firstQuestion, randomQuestionIds = self._gameQuestionInfoService.randomAndGetUserFirstQuestion(activeId)
		playInfo = self._userPlayOriginGameInfoService.addUserPlayInfo(userId, activeId, randomQuestionIds, firstQuestion['id'])
		if playInfo:
			return self._continuePlay(playInfo, firstQuestion)
		return self._handleIllegalResp(failedType="server")

	######如果用户未分享成功过，则弹出叫用户分享，否则，无法继续游戏，告诉用户
	def _sharedToPlay(self, playInfo):
		userId = playInfo['userId']
		activeId = playInfo['activeId']		
		activeInfo = self._gameActiveInfoService.getInfo(activeId)
		if activeInfo is None:
			return self._handleIllegalResp()
		info = self._userShareInfoService.getInfoByUserIdActiveId(userId, activeId)
		if info:
			###已经分享了 可以玩了
			if int(info['result']) == BizStatusUtils.SHARED_SUCCESS:
				return self._continuePlay(playInfo, activeInfo =  activeInfo)
			else:
				return self._handleNeedShareThenPlayResp(activeInfo, info)

		if not info:
			##获取用户分享的链接
			unionId = self._userInfoService.getUserUnionId(userId)
			if not unionId:
				return self._handleIllegalResp()
			LOGGER.debug("_sharedToPlay unionId:" + unionId)
			info = self._userShareInfoService.genShareInfo(userId, unionId, activeId, activeInfo['url'])
			if info is None:
				return self._handleIllegalResp()
			else:
				return self._handleNeedShareThenPlayResp(activeInfo, info)
	
	def _handleNeedShareThenPlayResp(self, activeInfo, shareInfo):
		###需要分享才能玩
		###
		# self._weixinService.sign(app.config.get['weixin_js_url'])
		return {'success': True, 'needShare': True, 'activeInfo': activeInfo, 'shareInfo': shareInfo}

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
		rightAnswer = self._gameQuestionInfoService.checkAnswer(questionId, answerId)
		if rightAnswer:
			return self._gotoNext(userId, activeId, questionId, playInfo)
		else:
			self._userPlayOriginGameInfoService.modifyResultFailedCount(playInfo['id'], \
						userId, activeId, BizStatusUtils.PLAY_RESULT_FAILED, 1)			
			playInfo = self._userPlayOriginGameInfoService.getInfo(userId, activeId)
			return self._handlePrePlay(playInfo)

	def shareGameNext(self, userId, activeId, shareCode, questionId, answerId):
		playInfo = self._userPlayShareGameInfoService.getInfo(userId, activeId, shareCode)
		if playInfo is None or int(playInfo['playQuestionId']) != int(questionId):
			return self._handleIllegalResp(message="No playinfo or the question id is wrong.")

		rightAnswer = self._gameQuestionInfoService.checkAnswer(questionId, answerId)
		if rightAnswer:
			return self._gotoSharedGameNext(userId, activeId, shareCode, questionId, playInfo)
		else:
			self._userPlayShareGameInfoService.modifyResult(playInfo['id'], \
						userId, activeId, shareCode, BizStatusUtils.PLAY_RESULT_FAILED)
			###失败了 没得玩
			return self._handelNoMoreCanPlayResp(activeId)

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
		if 'shareCode' in playInfo:
			return {'success': True, 'play': True, 'activeInfo': activeInfo, 'playInfo': playInfo, 'question': question, 'answers': answers, 'shareCode': playInfo['shareCode']}
		else:
			return {'success': True, 'play': True, 'activeInfo': activeInfo, 'playInfo': playInfo, 'question': question, 'answers': answers}

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

	def _userId(self, unionId):
		return self._userInfoService.getUserId(unionId)

