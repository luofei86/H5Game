# -*- coding: utf-8 -*-

###活动奖品信息

###1, 1, 1, 1等奖, iPhone6S   5
####
###id, active_id, level, level_desc, prize_desc, count, 
###自有id,活动id，奖品等级,奖品等级描述,奖品描述,奖品数量
####pk---id unique key  activeId-----level
class GameActivePrizeInfo:
	def __init__(self, id, activeId, level, levelDesc, prizeDesc, count):
		self.id = id
		self.activeId = activeId
		self.level = level
		self.levelDesc = levelDesc
		self.prizeDesc = prizeDesc
		self.count = count

	def __str__(self):
		return "ActivePrizeInfo: id=" + str(self.id) \
			+", activeId=" + self.activeId \
			+", level=" + self.level \
			+", levelDesc=" + str(self.levelDesc) \
			+", prizeDesc=" + self.prizeDesc \
			+", count=" + self.count