# -*- coding: utf-8 -*-

##游戏id,标题，展示资源地址，展示资源类型，游戏提示词，游戏所有可能答案id列表，游戏正确答案

class GameInfoModel:
	def __init__(self, id, title, res, res_type):
		self.id = id;
		self.title = title;
		self.res = res;
		slef.resType = res_type;

	def __str__(self):
		return self.type \
			+", id=" + self.id \
			+", title=" + self.title \
			+", res=" + self.res \
			+", resType=" + self.resType