# -*- coding: utf-8 -*-

###用户玩活动信息

####
###userId, activeId, question_ids, cur_play_question_id, faile_count, result

class UserPlayOriginGameInfo:
	def __init__(self, id, userId, activeId, questionIds, playQuestionId, failedCount, result):
		self.id = id
		self.userId = userId
		self.activeId = activeId
		self.questionIds = questionIds
		self.playQuestionId = playQuestionId
		self.failedCount = failedCount
		self.result = result