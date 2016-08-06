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

class WeixinService:
	def __init__(self, appId, appSecret):
		self.appId = appId
		self.appSecret = appSecret
		# self.ret = {
		# 	'nonceStr': self.__create_nonce_str(),
		# 	'jsapi_ticket': self._getJsApiTicket(),
		# 	'timestamp': self.__create_timestamp(),
		# 	'appId': appId,
		# 	'url': ''
		# }

	def __create_nonce_str(self):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

	def __create_timestamp(self):
		return int(time.time())

	def sign(self, url):
		if not url:
			return self.ret
		self.ret['url'] = url
		string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
		self.ret['signature'] = hashlib.sha1(string).hexdigest()
		return self.ret

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
			r.set(key, data['access_token'], data['expire_time'])
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
		print response
		access_token = json.loads(response.text)['access_token']
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
			r.set(key, data['jsapi_ticket'], data['expire_time'])
			return data['jsapi_ticket']

	def _buildJsApiTicketKey(self):
		return "api_ticket"

	def _getJsApiTicketDataDirect(self):
		url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token=%s" %\
				(self._getAccessToken())
		response = requests.get(url)
		LOGGER.debug(response)
		print response
		jsapi_ticket = json.loads(response.text)['jsapi_ticket']
		data = {}
		data['jsapi_ticket'] = jsapi_ticket
		data['expire_time'] = int(time.time()) + 7000
		return data

	# def getJsApiTicket(self):
	# 	json_file = open('jsapi_ticket.json')
	# 	data = json.load(json_file)
	# 	json_file.close()
	# 	jsapi_ticket = data['jsapi_ticket']
	# 	if data['expire_time'] < time.time():
	# 		url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token=%s" %\
	# 			(self.getAccessToken())
	# 		response = requests.get(url)
	# 		jsapi_ticket = json.loads(response.text)['ticket']
	# 		data['jsapi_ticket'] = jsapi_ticket
	# 		data['expire_time'] = int(time.time()) + 7000
	# 		json_file = open('jsapi_ticket.json', 'w')
	# 		json_file.write(json.dumps(data))
	# 		json_file.close()
	# 	return jsapi_ticket

	def getTechUsers(self):
		url = "https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s" % (self.getAccessToken())
		payload = {'tagid': self.getTagId(), 'next_openid': ''}
		headers = {'content-type': 'application/json'}
		response = requests.post(url, data=json.dumps(payload), headers=headers)
		data = response.json()
		print data
		openids = data['data']['openid']
		return openids

	def getTagId(self):
		set_data = open('set_data.json')
		data = json.load(set_data)
		set_data.close()
		if data['tagid']:
			return data['tagid']
		else:
			return 101

	def getUserInfo(self, openid):
		# https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
		url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" \
			% (self.getAccessToken(), openid)
		response = requests.get(url)
		return response.json()

	def getCurOpenId(self, code):
		url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" \
			% (self.appId, self.appSecret, code)
		response = requests.get(url)
		data = response.json()
		openid = data['openid']
		return openid

	def getQcodeUrl(self, oid):
		url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % (self.getAccessToken())
		payload = {'expire_seconds': 2591999, 'action_name': 'QR_SCENE', 'action_info': {"scene": {"scene_id": oid}}}
		headers = {'content-type': 'application/json'}
		response = requests.post(url, data=json.dumps(payload), headers=headers)
		data = response.json()
		ticket = data['ticket']
		# http://weixin.qq.com/q/zUipXRjlo7zaLJROUmaT
		# print data['url']
		url_qcode = "https://mp.weixin.qq.com/cgi-bin/showqrcode?"
		params = {'ticket': ticket}
		from urllib import urlencode
		# Content-Type:image/jpg
		return url_qcode + urlencode(params)
