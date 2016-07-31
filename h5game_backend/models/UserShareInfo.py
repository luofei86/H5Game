# -*- coding: utf-8 -*-


###
###用户分享信息
####用户Id, 活动id, 分享码, 分享地址, 分享标题，分享内容, 分享结果
###
class UserShareInfo:
	def __init__(self, userId, activeId, shareCode, shareUrl, title, content, result):
		self.userId = userId
		self.activeId = activeId
		self.shareCode = shareCode
		self.shareUrl = shareUrl
		self.title = title
		self.content = content
		self.result = result