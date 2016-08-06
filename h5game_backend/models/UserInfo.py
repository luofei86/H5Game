# -*- coding: utf-8 -*-


###用户信息表
######id, union_id, nickname, sex, city, headimgurl
######
class UserInfo:
	def __init__(self, id, unionId, nickname, sex, city, headimgurl):
		self.id = id
		self.unionId = unionId
		self.nickname = nickname
		self.sex = sex
		self.city = city
		self.headimgurl = headimgurl