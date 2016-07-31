# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import GameAnswerInfo

from h5game_backend import LOGGER

__author__ = 'luofei'

ALL_SQL = '''SELECT id, title, resource_url, resource_type FROM game_answer_info WHERE status = 0'''
IDS_SQL = ALL_SQL + ''' AND id in '''

class GameAnswerInfoDao:
	def queryInfos(self, ids):		
		idsStr = str(",".join(map(str,ids)))
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			sql = IDS_SQL + "(" + idsStr + ")"
			cur.execute(sql)
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
		return None

	def _toObject(self, db_item):
		if db_item is None:
			return None
		result = GameAnswerInfo(db_item[0], db_item[1], db_item[2], db_item[3])
		return result