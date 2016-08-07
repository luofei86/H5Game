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

WEINXIN_APITICKET_KEY = "weixin:api_ticket"
WEIXIN_ACCESSTOKEN_KEY ="weixin:access_token"


# self.ret = {
#             'nonceStr': self.__create_nonce_str(),
#             'jsapi_ticket': jsapi_ticket,
#             'timestamp': self.__create_timestamp(),
#             'url': url
#         }
class JsApiService:
	def __init__(self, appId, appSecret):
		self.appId = appId
		self.appSecret = appSecret
		self.signStr = {
			'nonceStr': self.__create_nonce_str(),
			'jsapi_ticket': self._getJsApiTicket(),
			'timestamp': self.__create_timestamp(),
			'url': ''		
		}


	def __create_nonce_str(self):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

	def __create_timestamp(self):
		return int(time.time())

	def sign(self, url):
		if not url:
			return self.signStr
		self.signStr['url'] = url
		string = '&'.join(['%s=%s' % (key.lower(), self.signStr[key]) for key in sorted(self.signStr)])
		LOGGER.debug(string)
		self.signStr['signature'] = hashlib.sha1(string).hexdigest()
		return self.signStr

	def _getAccessToken(self):		
		r = redis.StrictRedis(connection_pool = POOL)
		if(r):
			return self._getAccessTokenFromRedis(r)
		else:
			return self._getAccessTokenFromFile()

	def _getAccessTokenFromFile(self):	
		json_file = open('access_token.json')
		data = json.load(json_file)
		json_file.close()
		access_token = data['access_token']
		if data['expire_time'] < time.time():
			data = self._getAccessTokenDataDirect()
			return data['access_token']
		return access_token

	def _getAccessTokenFromRedis(self, r):		
		key = self._buildAccessTokeKey()
		result = r.get(key)
		if result:
			return result
		else:
			data = self._getAccessTokenDataDirect()
			r.setex(key, 7000, data['access_token'])
			return data['access_token']

	def _buildJsApiTicketKey(self):
		return WEINXIN_APITICKET_KEY

	def _buildAccessTokeKey(self):
		return WEIXIN_ACCESSTOKEN_KEY

	def _getAccessTokenDataDirect(self):
		url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" %\
							(self.appId, self.appSecret)
		response = requests.get(url)		
		LOGGER.debug(response)
		access_token = json.loads(response.text)['access_token']
		LOGGER.debug(access_token)
		data ={}
		data['access_token'] = access_token
		data['expire_time'] = int(time.time()) + 7000
		return data

	def _getJsApiTicket(self):		
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			return self._getJsApiTicketFromRedis(r)
		else:
			return self._getJsApiTicketFromFile()

	def _getJsApiTicketFromFile(self):	
		json_file = open('jsapi_ticket.json')
		data = json.load(json_file)
		json_file.close()
		jsapi_ticket = data['jsapi_ticket']
		if data['expire_time'] < time.time():
			data =  self._getJsApiTicketDataDirect()
			return data['jsapi_ticket']
		return jsapi_ticket

	def _getJsApiTicketFromRedis(self,r ):		
		key = self._buildJsApiTicketKey()
		result = r.get(key)
		if result:
			return result
		else:
			data = self._getJsApiTicketDataDirect()
			###
			r.setex(key, 7000, data['jsapi_ticket'])
			return data['jsapi_ticket']


#https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
	def _getJsApiTicketDataDirect(self):
		url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token=%s&type=jsapi" %\
				(self._getAccessToken())
		LOGGER.debug("Get ticket from url:" + url)
		response = requests.get(url)
		LOGGER.debug("Api tickent resp" + str(response))
		LOGGER.debug("Api tickent resp" + str(response.text))
		print response
		jsapi_ticket = json.loads(response.text)['ticket']
		data = {}
		data['jsapi_ticket'] = jsapi_ticket
		data['expire_time'] = int(time.time()) + 7000
		return data

