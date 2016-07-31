# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import GameActivePrizeInfo

#####活动奖品dao
###id, active_id, level, level_desc, prize_desc, count, 
__author__ = 'luofei'


TABLE_NAME= " game_active_prize_info "
COLUMNS = " id, active_id, level, level_desc, prize_desc, count  "
ALL_SQL = '''SELECT ''' + COLUMNS + ''' FROM ''' + TABLE_NAME + ''' WHERE status = 0'''
ID_SQL = ALL_SQL + ''' AND id = %s '''
IDS_SQL = ALL_SQL + ''' AND id in (%s) '''
ACTIVEID_SQL = ALL_SQL + ''' AND active_id = %s ORDER BY level'''


class GameActivePrizeInfoDao:
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

	def queryInfosByActiveId(self, activeId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ACTIVEID_SQL, (str(activeId),))
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

##
	def queryInfos(self, ids):
		format_ids_strings = ','.join(['%s']) * len(ids)
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(IDS_SQL, (format_ids_strings, tuple(ids)))
			result = cur.fetchone()
		return self._toObject(result)

	def queryInfo(self, id):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ID_SQL, (str(id),))
			result = cur.fetchone()
		return self._toObject(result)

#######id, active_id, level, level_desc, prize_desc, count, 
	def _toObject(self, db_item):
		if db_item is None:
			return None
		return GameActivePrizeInfo(db_item[0], db_item[1], db_item[2], db_item[3], 
								db_item[4], db_item[5])
