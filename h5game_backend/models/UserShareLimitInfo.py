# -*- coding: utf-8 -*-



####用户分享限制表   每个用户每个活动只能分享二次
#######userId activeId  unique key
class UserShareLimitInfo:
	def __init__(self, id, userId, activeId, shareCount):
		self.id = id
		self.userId = userId
		self.activeId = activeId
		self.shareCount = shareCount
