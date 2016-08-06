# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserShareInfo

__author__ = 'luofei'

TABLE_NAME = " user_share_info "
COLUMNS = " id, user_id, active_id, share_code, share_url, title, content, result "
#ALL_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE `status` = 0 order by id LIMIT %s, %s'''
SHARCODE_UK_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE share_code = %s'''
USER_ACTIVE_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE user_id = %s AND active_id = %s'''
ID_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE `id` = %s'''
INSERT_SQL = '''INSERT INTO ''' + TABLE_NAME + ''' (`id`, `user_id`, `active_id`, `share_code`, ''' \
		 		+ '''`share_url`, `title`, `content`, `result`, `status`, update_time, create_time) ''' \
				+ '''VALUES(NULL, %s, %s, %s, %s, %s, %s, 0, 0, now(), now())'''
UPDATE_RESULT_SQL = '''UPDATE ''' + TABLE_NAME + ''' SET `result` = %s WHERE id = %s'''

class UserShareInfoDao:
	
	##def __init__(self, userId, activeId, shareCode, shareUrl, title, content, result):
	
	def insert(self, userId, activeId, shareCode, shareUrl, title, content):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(userId), str(activeId), str(shareCode), \
					str(shareUrl), str(title), str(content)))
			dbConn.commit()

	def updateResult(self, id, result):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UPDATE_RESULT_SQL, (str(result), str(id)))
		dbConn.commit()

	def queryInfo(self, id):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ID_SQL, (str(id),))
			result = cur.fetchone()
		if result is None:
			return None		
		return self._toObject(result)

	def queryInfoByShareCode(self, shareCode):		
		dbConn = get_db()		
		with closing(dbConn.cursor()) as cur:
			cur.execute(SHARCODE_UK_SQL, (str(shareCode),))
			result = cur.fetchone()
		if result is None:
			return None
		return self._toObject(result)

	def queryInfoByUserIdActiveId(self, userId, activeId):
		dbConn = get_db()		
		with closing(dbConn.cursor()) as cur:
			cur.execute(USER_ACTIVE_SQL, (str(userId), str(activeId)))
			result = cur.fetchone()
		if result is None:
			return None
		return self._toObject(result)

	def _toObject(self, db_item):
		if db_item is None:
			return None
		return UserShareInfo(db_item[0], db_item[1], db_item[2], db_item[3], \
							db_item[4], db_item[5], db_item[6], db_item[7])

