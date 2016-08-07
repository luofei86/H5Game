# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import WeiXinAccessToken

__author__ = 'luofei'


##############access_token, expire_time----int value will expire and this time
TABLE_NAME= " weixin_accesstoken "
COLUMNS = " access_token, expire_time "
INSERT_SQL = '''INSERT INTO ''' + TABLE_NAME + ''' (access_token, expire_time, status, update_time, create_time) ''' \
			+ ''' VALUES (%s, %s, 0, now(), now()) '''
LATEST_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' ORDER BY create_time DESC LIMIT 1'''

class WeiXinAccessTokenDao:
	def insert(self, access_token, expire_time):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(access_token), str(expire_time)))
		dbConn.commit()

	def queryLatestInfo(self):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(LATEST_SQL)
			result = cur.fetchone()
		if result is None:
			return None
		return  self._toObject(result)
	

	def _toObject(self, db_item):
		if db_item is None:
			return None
		return WeiXinAccessToken(db_item[0], db_item[1])
