# -*- coding: utf-8 -*-

from flask import render_template
from .. import app


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('404.html'),404


@app.errorhandler(403)
def page_not_found(error):
    app.logger.error(error)
    return render_template('404.html'),403

@app.errorhandler(500)
def some_error(error):
    app.logger.error(error)
    return render_template('404.html'),500