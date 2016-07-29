# -*- coding: utf-8 -*-

##游戏id,标题，展示资源地址，展示资源类型，游戏提示词，游戏所有可能答案id列表，游戏正确答案

class GameInfoModel:
	def __init__(self, gameId, gameTitle, gameResource, gameResurceType, gameTipWord, allAnswerIds, rightAnswerId):
		self.gameId = gameId;
		self.allAnswerIds = allAnswerIds;
		self.rightAnswerId = rightAnswerId;
		self.gameTitle = gameTitle;
		slef.gameResource = gameResource;
		self.gameResurceType = gameResurceType;

	def __str__(self):
		return self.type \
			+", gameId=" + self.gameId \
			+", gameTitle=" + self.gameTitle \
			+", gameResource=" + self.gameResource \
			+", gameResurceType=" + self.gameResurceType \
			+", allAnswerIds=" + self.allAnswerIds \
			+", rightAnswerId=" + self.rightAnswerId