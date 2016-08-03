# -*- coding: utf-8 -*-

import datetime
from flask import url_for
from h5game_backend import app


@app.template_filter()
def timestamp_strftime(timestaamp):
    return datetime.datetime.fromtimestamp(int(timestaamp)).strftime("%Y-%m-%d");
