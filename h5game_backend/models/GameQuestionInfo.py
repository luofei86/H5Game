# -*- coding: utf-8 -*-

##游戏id,标题，展示资源地址，展示资源类型，游戏提示词，游戏所有可能答案id列表，游戏正确答案


#(db_item['id'], db_item['title'], 
#db_item['resource_url'], db_item['resource_type'], 
#db_item['possible_answer_ids'], db_item['right_answer_id'],
#db_item['tips'])
class GameQuestionInfo:
	def __init__(self, id, activeId, title, resourceUrl, resourceType, possibleAnswerIds, rightAnswerId, tips):
		self.id = id
		self.activeId = activeId
		self.title = title
		self.resourceUrl = resourceUrl
		self.resourceType = resourceType
		self.possibleAnswerIds = possibleAnswerIds
		self.rightAnswerId = rightAnswerId
		self.tips = tips

	def __str__(self):
		return "GameQuestionInfo: id=" + str(self.id) \
			+", activeId=" + self.activeId \
			+", title=" + self.title \
			+", resourceUrl=" + self.resourceUrl \
			+", resourceType=" + str(self.resourceType) \
			+", possibleAnswerIds=" + self.possibleAnswerIds \
			+", rightAnswerId=" + str(self.rightAnswerId) \
			+", tips=" + self.tips