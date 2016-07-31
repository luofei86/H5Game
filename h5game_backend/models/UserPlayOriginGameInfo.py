# -*- coding: utf-8 -*-

###用户玩活动信息

####
###userId, activeId, question_ids, cur_play_question_id, result

class UserPlayOriginGameInfo:
	def __init__(self, userId, activeId, questionIds, playQuestionId, result):
		self.userId = userId
		self.activeId = activeId
		self.questionIds = questionIds
		self.playQuestionId = playQuestionId
		self.result = result

	def __str__(self):
		return "UserPlayInfo: userId=" + self.userId \
			+", activeId=" + self.activeId \
			+", result=" + self.result