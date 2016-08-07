# -*- coding: utf-8 -*-

#######access_token, expire_time----int value will expire and this time
class WeiXinAccessToken:
	def __init__(self, access_token, expire_time):
		self.access_token = access_token
		self.expire_time = expire_time
