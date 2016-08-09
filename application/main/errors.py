# -*- coding: utf-8 -*-
from application.main import main
from flask import render_template


@main.route('/test')
def test():
    return 'OK'


@main.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@main.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
