# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserInfo

__author__ = 'luofei'

TABLE_NAME= " user_info "
COLUMNS = " id, open_id, union_id, nickname, sex, language, city, province, country, headimgurl"
INSERT_SQL = '''INSERT INTO ''' + TABLE_NAME + ''' (''' \
		+ COLUMNS + ''', status, update_time, create_time) ''' \
		+ ''' VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, NOW(), NOW()) ''' \
		+ ''' ON DUPLICATE KEY UPDATE ''' \
		+ ''' nickname = %s , headimgurl = %s '''


UK_SQL = '''SELECT `id`, `open_id` FROM ''' + TABLE_NAME + ' WHERE status = 0 AND open_id = %s '''
UK_ID_SQL = '''SELECT id FROM ''' + TABLE_NAME + ''' WHERE status = 0 AND open_id = %s '''
OPENID_SQL = '''SELECT open_id FROM ''' + TABLE_NAME + ''' WHERE status = 0 AND id = %s '''


class UserInfoDao:
	def insert(self, openId, unionId, nickname, sex, language, city, province, country, headimgurl):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(openId),str(unionId), str(nickname), str(sex), \
				+ str(language), str(city), str(province), str(country), str(headimgurl), \
				+ str(nickname), str(headimgurl)))
			dbConn.commit()

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
		return UserInfo(db_item[0], db_item[1])
