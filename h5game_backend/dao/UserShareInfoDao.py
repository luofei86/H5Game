# # -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserShareInfo

__author__ = 'luofei'

TABLE_NAME = " user_share_info "
ALL_SQL = '''SELECT active_id， share_code FROM ''' + TABLE_NAME + ''' WHERE `status` = 0 AND result = 1 order by id LIMIT %s, %s'''
UK_SQL = '''SELECT active_id FROM ''' + TABLE_NAME + ''' WHERE `status` = 0 AND result = 1 AND share_code = %s'''
SHARED_SQL = '''SELECT id FROM ''' + TABLE_NAME + '''WHERE status = 0 AND user_id = %s AND active_id = %s AND result = %s'''

INSERT_SQL = '''INSERT IGNORE INTO ''' + TABLE_NAME + ''' (`id`, `user_id`, `active_id`, `share_code`, ''' \
		 		+ '''`share_url`, `title`, `content`, `result`, `status`, update_time, create_time) ''' \
				+ '''VALUES(NULL, %s, %s, %s, %s, %s, %s, 0, 0, now(), now())'''
UPDATE_SQL = '''UPDATE ''' + TABLE_NAME + ''' SET `result` = %s WHERE share_code = %s'''

class UserShareInfoDao:
	
	##def __init__(self, userId, activeId, shareCode, shareUrl, title, content, result):
	
	def insert(self, userId, activeId, shareCode, shareUrl, title, content):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(userId), str(activeId), str(shareCode), \
					str(shareUrl), str(title), str(content)))
			dbConn.commit()

	def updateResult(self, shareCode, result):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UPDATE_SQL, (str(result), str(shareCode)))
		dbConn.commit()

	def queryId(self, userId, activeId, result):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(SHARED_SQL, (str(userId), str(activeId), str(result)))

	def queryActiveIdByShareCode(self, shareCode):
		dbConn = get_db()		
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(shareCode),))
			result = cur.fetchone()
		if result is None:
			return None
		return result[0]