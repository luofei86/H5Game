# -*- coding: utf-8 -*-

##游戏答案模型id,标题，展示资源地址，展示资源类型，游戏提示词，游戏所有可能答案id列表，游戏正确答案

class GameAnswerInfo:
	def __init__(self, id, title, resourceUrl, resourceType):
		self.id = id
		self.title = title
		self.resourceUrl = resourceUrl
		self.resourceType = resourceType