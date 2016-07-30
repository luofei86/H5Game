# -*- coding: utf-8 -*-


###用户抽奖码信息

###id, token, active_info_id, bouns_code, 
class UserBounsInfo:
	def __init__(self, id, title, resourceUrl, resourceType, possibleAnswerIds, rightAnswerId, tips):
		self.id = id
		self.title = title
		self.resourceUrl = resourceUrl
		self.resourceType = resourceType
		self.possibleAnswerIds = possibleAnswerIds
		self.rightAnswerId = rightAnswerId
		self.tips = tips

	def __str__(self):
		return "GameQuestionInfo: id=" + str(self.id) \
			+", title=" + self.title \
			+", resourceUrl=" + self.resourceUrl \
			+", resourceType=" + str(self.resourceType) \
			+", possibleAnswerIds=" + self.possibleAnswerIds \
			+", rightAnswerId=" + str(self.rightAnswerId) \
			+", tips=" + self.tips