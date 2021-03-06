# -*- coding: utf-8 -*-

import json
import time
import requests
import random
import string
import hashlib
import redis

from h5game_backend import POOL
from h5game_backend import LOGGER

class WeixinService:
	def __init__(self, appId, appSecret):
		self.appId = appId
		self.appSecret = appSecret

	def getOpenInfo(self, code):
		url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" \
			% (self.appId, self.appSecret, code)
		response = requests.get(url)
		data = response.json()
		LOGGER.debug("Get open info with code: %s return: %s." % (str(code), str(data)))
		if data is None or hasattr(data, 'errcode'):
			return None
		openId = data['openid']
		accessToken = data['access_token']
		if not openId or not accessToken:
			return None
		return data

#https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN

	def refreshOpenInfo(self, code, refreshCode):
		url = "https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s" \
			% (self.appId, refreshCode)
		response = requests.get(url)
		data = response.json()
		LOGGER.debug("Refresh open info by code: %s and refreshCode %s  return: %s." % (str(code), str(refreshCode), str(data)))
		if data is None:
			return None
		openId = data['openid']
		accessToken = data['access_token']
		if not openId or not accessToken:
			return None
		return data

#https://api.weixin.qq.com/sns/userinfo?access_token=WyaAVSk-C-mA1aHSzcO-H4rZ9zFTeWWoWh-j5ZO_nmX9VIXnN1M3jXxpeeKWU-Au8QMIcbD4McWcLlQ0hiBFUTDl6Cqlt8dRWyw7enPJCPQ&openid=o8Y11v1BJZx0vCCML56YBPonoo2U&lang=zh_CN
	def getUserInfo(self, openId, accessToken):
		url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" \
				% (accessToken, openId)
		response = requests.get(url)
		response.encoding = "utf-8"
		data = response.json()
		LOGGER.debug("Get user info with openId: %s and accessToken: %s return: %s." % (str(openId), str(accessToken), str(data)))
		return data
