# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserPrizeInfo

#####用户中奖信息
####(self, id, userId, activeId, prizeCode):
__author__ = 'luofei'


#######id, keyword, signWord, url, title content, resource_url
TABLE_NAME= " user_prize_info "
COLUMNS = " user_id, active_id, prize_code "
INSERT_SQL = '''INSERT INTO ''' + TABLE_NAME + ''' (id, user_id, active_id, prize_code, status, update_time, create_time) ''' \
			+ ''' VALUES(null, %s, %s, %s, 0, now(), now()) '''
ALL_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE status = 0'''
UK_SQL = ALL_SQL + ''' AND user_id = %s AND active_id = %s '''

class UserPrizeInfoDao:
	def insert(self, userId, activeId, prizeCode):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(userId), str(activeId), str(prizeCode)))
		dbConn.commit()

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
	

	def queryInfoByUk(self, userId, activeId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(userId), str(activeId)))
			result = cur.fetchone()
		return self._toObject(result)

#######id, keyword, sign_word, url, title content, resource_url
	def _toObject(self, db_item):
		if db_item is None:
			return None
		return UserPrizeInfo(db_item[0], db_item[1], db_item[2])
