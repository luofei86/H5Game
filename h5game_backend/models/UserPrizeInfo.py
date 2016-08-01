# -*- coding: utf-8 -*-


###用户抽奖码信息

###id, userId, active_info_id, bouns_code, 
class UserPrizeInfo:
	def __init__(self, userId, activeId, prizeCode):
		self.userId = openId
		self.activeId = activeId
		self.prizeCode = prizeCode

	def __str__(self):
		return "UserPrizeInfo: userId=" + str(self.userId) \
			+", activeId=" + self.activeId \
			+", prizeCode=" + self.prizeCode