# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserInfo

__author__ = 'luofei'


#用户信息表

TABLE_NAME= " user_info "
COLUMNS = " id, open_id, nickname, sex, city, headimgurl "
ALL_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE status = 0 '''
UK_SQL = ALL_SQL + ''' AND open_id = %s '''
UK_ID_SQL = '''SELECT id FROM ''' + TABLE_NAME + ''' WHERE status = 0 AND open_id = %s '''
OPENID_SQL = '''SELECT open_id FROM ''' + TABLE_NAME + ''' WHERE status = 0 AND id = %s '''

class UserInfoDao:
	def queryInfoById(self, id):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(id),))
			result = cur.fetchone()
		return self._toObject(result)

	def queryInfoByUk(self, openId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(openId),))
			result = cur.fetchone()
		return self._toObject(result)

	def queryOpenId(self, id):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(OPENID_SQL, (str(id),))
			result = cur.fetchone()
			if result:
				return result[0]
		return None

	def queryIdByUk(self, openId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_ID_SQL, (str(openId), ))
			result = cur.fetchone()
			if result:
				return result[0]
		return None


	def _toObject(self, db_item):
		if db_item is None:
			return None
		return UserInfo(db_item[0], db_item[1], db_item[2], db_item[3], db_item[4], db_item[5])
