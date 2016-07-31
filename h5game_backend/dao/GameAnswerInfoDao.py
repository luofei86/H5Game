# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import GameAnswerInfo

__author__ = 'luofei'

ALL_SQL = '''SELECT id, title, resource_url, resource_type FROM game_answer_info WHERE status = 0'''
IDS_SQL = ALL_SQL + ''' AND id in (%s) '''

class GameAnswerInfoDao:
	def queryAllInfos(self):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ALL_SQL)
			retlist = cur.fetchall()
			dbConn.commit()
		return retlist

	def queryInfos(self, ids):		
		idsStr = ",".join(map(str,ids))
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(IDS_SQL, (idsStr,))
			result = cur.fetchone()
		return self._toObject(result)

	def _toObject(self, db_item):
		if db_item is None:
			return None
		result = GameAnswerInfo(db_item[0], db_item[1], db_item[2], db_item[3])
		return result