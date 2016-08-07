# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import WeiXinJsApiTicket

__author__ = 'luofei'


##############jsapi_ticket, expire_time----int value will expire and this time
TABLE_NAME= " weixin_apiticket "
COLUMNS = " jsapi_ticket, expire_time "
INSERT_SQL = '''INSERT INTO ''' + TABLE_NAME + ''' (jsapi_ticket, expire_time, status, update_time, create_time) ''' \
			+ ''' VALUES (%s, %s, 0, now(), now()) '''
LATEST_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' ORDER BY create_time DESC LIMIT 1'''

class WeiXinJsApiTicketDao:
	def insert(self, jsapi_ticket, expire_time):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(jsapi_ticket), str(expire_time)))
		dbConn.commit()

	def queryLatestInfo(self):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(LATEST_SQL)
			result = cur.fetchone()
		if not result:
			return None
		return  self._toObject(result)
	

	def _toObject(self, db_item):
		if db_item is None:
			return None
		return WeiXinJsApiTicket(db_item[0], db_item[1])
