# -*- coding: utf-8 -*-


###用户信息表
######id, open_id, nickname, sex, city, headimgurl
######
# weiXinInfo['openid'], weiXinInfo['nickname'], weiXinInfo['sex'], \
# 						weiXinInfo['language'], weiXinInfo['city'], weiXinInfo['province'], \
# 						weiXinInfo['country'], weiXinInfo['headimgurl'], weiXinInfo['unionid']
class UserInfo:
	def __init__(self, id, openId):
		self.id = id
		self.openId = openId