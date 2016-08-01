# -*- coding: utf-8 -*-

###用户玩玩家分享的活动信息

####
###userId, activeId, shareCode, questionIds, playQuestionId, result

class UserPlayShareGameInfo:
	def __init__(self, id, userId, activeId, shareCode, questionIds, playQuestionId, result):
		self.id = id
		self.userId = userId
		self.activeId = activeId
		self.shareCode =shareCode
		self.questionIds = questionIds
		self.playQuestionId = playQuestionId
		self.result = result

	def __str__(self):
		return "UserPlayShareInfo: userId=" + self.userId \
			+", activeId=" + self.activeId \
			+", questionIds=" + self.questionIds \
			+", playQuestionId=" + self.playQuestionId \
			+", result=" + self.result