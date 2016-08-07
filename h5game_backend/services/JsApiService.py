# -*- coding: utf-8 -*-

import json
import time
import requests
import random
import string
import hashlib
import redis

from dao.WeiXinJsApiTicketDao import *
from dao.WeiXinAccessTokenDao import *

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
		self._ticketDao = WeiXinJsApiTicketDao()
		self._accessTokenDao = WeiXinAccessTokenDao()
		self.appId = appId
		self.appSecret = appSecret
		self.signStr = {
			'nonceStr': self.__create_nonce_str(),
			'jsapi_ticket': self._getJsApiTicket(),
			'timestamp': self.__create_timestamp(),
			'url': ''		
		}

	def sign(self, url):
		if not url:
			return self.signStr
		if not self.signStr['jsapi_ticket']:
			return None
		self.signStr['url'] = url
		string = '&'.join(['%s=%s' % (key.lower(), self.signStr[key]) for key in sorted(self.signStr)])
		LOGGER.debug('Sign str:' + string)
		self.signStr['signature'] = hashlib.sha1(string).hexdigest()
		return self.signStr

	def _getAccessToken(self):
		r = redis.StrictRedis(connection_pool = POOL)
		accessToken = None
		if r:
			key = self._buildAccessTokeKey()
			accessToken = r.get(key)
		if not accessToken:
			dbData = self._accessTokenDao.queryLatestInfo()
			if dbData and int(dbData.expire_time) > time.time():
				accessToken = dbData.access_token
				if r:
					self._initAndExpireKeyCacheInfo(r, key, accessToken, int(dbData.expire_time) - time.time())
		if not accessToken:
			while not self._lockToken():
				time.sleep(5)
				otherThreadData = self._getAccessToken()
				if otherThreadData:
					return otherThreadData
			try:
				apiData = self._getAccessTokenDataDirect()
				if apiData:
					accessToken = apiData['access_token']
					self._accessTokenDao.insert(apiData['access_token'], apiData['expire_time'])
					if r:
						self._initAndExpireKeyCacheInfo(r, key, accessToken, int(apiData['expire_time']) - time.time())
			finally:
				self._unlockToken()
		return accessToken

	def _getAccessTokenDataDirect(self):
		url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" %\
							(self.appId, self.appSecret)
		response = requests.get(url)
		LOGGER.debug("ticket api resp:" + str(response.text))
		respData = json.loads(response.text)
		if respData['access_token']:
			data = {}
			data['access_token'] = respData['access_token']
			data['expire_time'] = int(time.time()) + int(respData['expires_in'])
			return data
		return None

	def _getJsApiTicket(self):
		r = redis.StrictRedis(connection_pool = POOL)
		jsApiTicet = None
		if r:
			key = self._buildJsApiTicketKey()
			jsApiTicet = r.get(key)
		if not jsApiTicet:
			dbData = self._ticketDao.queryLatestInfo()
			if dbData and int(dbData.expire_time) > time.time():
				jsApiTicet = dbData.jsapi_ticket
				if r:
					self._initAndExpireKeyCacheInfo(r, key, jsApiTicet, int(dbData.expire_time) - time.time())
		if not jsApiTicet:
			while not self._lockTicket():
				time.sleep(5)
				otherThreadData = self._getJsApiTicket()
				if otherThreadData:
					return otherThreadData
			try:				
				apiData = self._getJsApiTicketDataDirect()
				if apiData:
					jsApiTicet = apiData['jsapi_ticket']
					self._ticketDao.insert(apiData['jsapi_ticket'], apiData['expire_time'])
					if r:
						self._initAndExpireKeyCacheInfo(r, key, jsApiTicet, int(apiData['expire_time']) - time.time())
			finally:
				self._unlockTicket()
		return jsApiTicet

	def _lockTicket(self):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = "ticket_lock"
			ret =  r.setnx(key, 1)
			return int(ret) == 1
		return True

	def _unlockTicket(self):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = "ticket_lock"
			ret =  r.delete(key)


	def _lockToken(self):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = "token_lock"
			ret =  r.setnx(key, 1)
			return int(ret) == 1
		return True

	def _unlockToken(self):
		r = redis.StrictRedis(connection_pool = POOL)
		if r:
			key = "token_lock"
			ret =  r.delete(key)

#https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
	def _getJsApiTicketDataDirect(self):
		url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token=%s&type=jsapi" %\
				(self._getAccessToken())
		LOGGER.debug("Get ticket from url:" + url)
		response = requests.get(url)
		LOGGER.debug("ticket api resp:" + str(response.text))
		respData = json.loads(response.text)
		if respData['ticket']:
			data = {}
			data['jsapi_ticket'] = respData['ticket']
			data['expire_time'] = int(time.time()) + int(respData['expires_in'])
			return data
		return None

	def _buildJsApiTicketKey(self):
		return WEINXIN_APITICKET_KEY

	def _buildAccessTokeKey(self):
		return WEIXIN_ACCESSTOKEN_KEY

	def _initAndExpireKeyCacheInfo(self, r, key, value, expireSeconds):
		if int(expireSeconds) >0 and r:
			r.setex(key, int(expireSeconds), value)


	def __create_nonce_str(self):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

	def __create_timestamp(self):
		return int(time.time())


