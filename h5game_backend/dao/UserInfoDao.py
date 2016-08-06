# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserInfo

__author__ = 'luofei'


#用户信息表

TABLE_NAME= " user_info "
COLUMNS = " id, union_id, nickname, sex, city, headimgurl "
INSERT_SQL = '''INSERT IGNORE INTO ''' + TABLE_NAME + ''' (id, ''' \
		+ ''' `union_id`, `nickname`, `sex`, `city`, `headimgurl`, status, update_time, create_time) ''' \
		+ ''' VALUES(null, %s, %s, %s, %s, %s, 0, NOW(), NOW()) '''
ALL_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE status = 0 '''
UK_SQL = ALL_SQL + ''' AND union_id = %s '''
UK_ID_SQL = '''SELECT id FROM ''' + TABLE_NAME + ''' WHERE status = 0 AND union_id = %s '''
UNIONID_SQL = '''SELECT union_id FROM ''' + TABLE_NAME + ''' WHERE status = 0 AND id = %s '''

class UserInfoDao:
	def insert(self, unionId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(unionId), '', '', '', ''))
			dbConn.commit()

	def queryInfoById(self, id):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(id),))
			result = cur.fetchone()
		return self._toObject(result)

	def queryInfoByUk(self, unionId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(unionId),))
			result = cur.fetchone()
		return self._toObject(result)

	def queryUnionId(self, id):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UNIONID_SQL, (str(id),))
			result = cur.fetchone()
			if result:
				return result[0]
		return None

	def queryIdByUk(self, unionId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_ID_SQL, (str(unionId), ))
			result = cur.fetchone()
			if result:
				return result[0]
		return None


	def _toObject(self, db_item):
		if db_item is None:
			return None
		return UserInfo(db_item[0], db_item[1], db_item[2], db_item[3], db_item[4], db_item[5])
