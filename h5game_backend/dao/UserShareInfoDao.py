# # -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserShareInfo

__author__ = 'luofei'

class UserShareInfoDao:
	__TABLE_NAME = "user_share_info"
	##def __init__(self, userId, activeId, shareCode, shareUrl, title, content, result):
	__ALL_SQL = '''SELECT active_id， share_code FROM ''' + __TABLE_NAME + ''' WHERE `status` = 0 AND result = 1 order by id LIMIT %s, %s'''
	__UK_SQL = '''SELECT active_id FROM ''' + __TABLE_NAME + ''' WHERE `status` = 0 AND result = 1 AND share_code = %s'''
	__INSERT_SQL = '''INSERT IGNORE INTO ''' + __TABLE_NAME + ''' (`id`, `user_id`, `active_id`, `share_code`, ''' \
		 		+ '''`share_url`, `title`, `content`, `result`, `status`, update_time, create_time) ''' \
				+ '''VALUES(NULL, %s, %s, %s, %s, %s, %s, 0, 0, now(), now())'''
	__UPDATE_SQL = '''UPDATE ''' + __TABLE_NAME + ''' SET `result` = %s WHERE share_code = %s'''

	def insert(self, userId, activeId, shareCode, shareUrl, title, content):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(self.__INSERT_SQL, (str(userId), str(activeId), str(shareCode), \
					str(shareUrl), str(title), str(content)))
			dbConn.commit()

	def updateResult(self, shareCode, result):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
				cur.execute(self.__UPDATE_SQL, (str(result), str(shareCode)))
				dbConn.commit()

	def queryAllInfos(self, start, size):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(self.__ALL_SQL, (str(start), str(size)))
			result = cur.fetchall()
		if result is None:
			return None
		values = []
		for r in result:
			value = self._toObject(r)
			if value is None:
				continue
			values.append(value)
		return value

	def queryActiveIdByShareCode(self, shareCode):
		dbConn = get_db()		
		with closing(dbConn.cursor()) as cur:
			cur.execute(self.__UK_SQL, (str(shareCode),))
			result = cur.fetchone()
		if result is None:
			return None
		return result[0]


##def __init__(self, userId, activeId, shareCode, shareUrl, title, content, result):
	def _toObject(self, db_item):
		if db_item is None:
			return None
		result = UserShareInfo(db_item[0], db_item[1])
		return result