# -*- coding: utf-8 -*-


###用户信息表
######id, open_id, nickname, sex, city, headimgurl
######
class UserInfo:
	def __init__(self, id, openId, nickname, sex, city, headimgurl):
		self.id = id
		self.openId = openId
		self.nickname = nickname
		self.sex = sex
		self.city = city
		self.headimgurl = headimgurl