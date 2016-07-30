# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import GameActiveInfo

#####关键字对应访问游戏地址
####(self, id, keyword, signWord, url):
__author__ = 'luofei'


#######id, keyword, signWord, url, title content, resource_url
TABLE_NAME= " game_active_info "
COLUMNS = " id, keyword, sign_word, url, title, content, resource_url "
ALL_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE status = 0'''
ID_SQL = ALL_SQL + ''' AND id = %s '''
UK_SQL = ALL_SQL + ''' AND sign_word = %s '''

class GameActiveInfoDao:
	def queryAllInfos(self):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ALL_SQL)
			result = cur.fetchall()
		if result is None:
			return None
		values = []
		for r in result:
			value = self._toObject(r)
			if value is None:
				continue
			values.append(value)
		return values

	def queryInfo(self, id):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ID_SQL, (str(id),))
			result = cur.fetchone()
		return self._toObject(result)

	def queryInfoByUk(self, signWord):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(signWord),))
			result = cur.fetchone()
		return self._toObject(result)

#######id, keyword, sign_word, url, title content, resource_url
	def _toObject(self, db_item):
		if db_item is None:
			return None
		return GameActiveInfo(db_item[0], db_item[1], db_item[2], db_item[3], 
								db_item[4], db_item[5], db_item[6])
