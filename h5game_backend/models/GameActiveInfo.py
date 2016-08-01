# -*- coding: utf-8 -*-


###关键字----游戏地址模型
###用来用户在公众号里输入关键字后返回对应的url地址

######id, keyword, signWord, url, title content, resource_url
######
class GameActiveInfo:
	def __init__(self, id, keyword, signWord, url, title, content, resourceUrl, prizeTime):
		self.id = id
		self.keyword = keyword
		self.signWord = signWord
		self.url = url
		self.title = title
		self.content = content
		self.resourceUrl = resourceUrl
		self.prizeTime = prizeTime

	def __str__(self):
		return "id=" + self.id \
			+", keyword=" + self.keyword \
			+", signWord=" + self.signWord \
			+", url=" + self.url \
			+", title=" + self.title \
			+", content=" + self.content \
			+", resourceUrl=" + self.resourceUrl