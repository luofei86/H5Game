# -*- coding: utf-8 -*-

import datetime
from time import mktime


###关键字----游戏地址模型
###用来用户在公众号里输入关键字后返回对应的url地址

######id, keyword, signWord, url, title content, resource_url
######
class GameActiveInfo:
	def __init__(self, id, championName, championUrl, keyword, signWord, url, title, content, resourceUrl, posterUrl, prizeTime):
		self.id = id
		self.championName = championName
		self.keyword = keyword
		self.signWord = signWord
		self.url = url
		self.title = title
		self.content = content
		self.resourceUrl = resourceUrl
		self.posterUrl = posterUrl
		self.championUrl = championUrl
		if isinstance(prizeTime, datetime.datetime):
			self.prizeTime = int(mktime(prizeTime.timetuple()))
		else:
			self.prizeTime = prizeTime