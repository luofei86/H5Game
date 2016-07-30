# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserShareLimitInfo

__author__ = 'luofei'

TABLE_NAME = 'user_share_limit_info'

QUERY_STR = "id, user_id, active_id, share_count FROM " + TABLE_NAME
ALL_LIMIT_SQL = '''SELECT ''' + QUERY_STR + ''' WHERE status = 0 ORDER BY `id` LIMIT %s, %s'''
UK_SQL = '''SELECT ''' + QUERY_STR + ''' WHERE status = 0 AND user_id = %s AND active_id = %s'''
INSERT_UPDATE_SQL = '''INSERT INTO ''' + TABLE_NAME + ''' (id, user_id, active_id, share_count, status, update_time, create_time)''' \
					+ ''' VALUES(NULL, %s, %s, 1, 0, now(), now()) ON DUPLICATE KEY UPDATE ''' \
					+ ''' share_count = IF(share_count > %s, share_count, share_count + 1) '''
UPDATE_SQL = '''UPDATE ''' + TABLE_NAME + ''' SET `share_count` = IF(`share_count` > 0, `share_count` - 1, 0) ''' \
			+ ''' WHERE user_id = %s AND active_id = %s '''


###用户分享限制表
class UserShareLimitInfoDao:
	def queryInfos(self,  start, size):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ALL_LIMIT_SQL, (str(start), str(size)))
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

	def queryInfo(self,  userId, activeId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(userId), str(activeId)))
			result = cur.fetchone()
		return self._toObject(result)

	def insertOrIncrUpdateCount(self, userId, activeId, maxLimit):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_UPDATE_SQL, (str(userId), str(activeId), str(maxLimit)))
			dbConn.commit()
			result = cur.fetchone()
		return result

	def decrUpdateCount(self, userId, activeId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UPDATE_SQL, (str(userId), str(activeId)))
			dbConn.commit()


	def _toObject(self, db_item):
		if db_item is None:
			return None

		result = UserShareLimitInfo(db_item[0], db_item[1], db_item[2], db_item[3])
		return result
