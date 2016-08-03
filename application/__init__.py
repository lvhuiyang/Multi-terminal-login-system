# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.index'


def create_app(config_name):
    """
    flask的工厂函数，用于创建flask应用、初始化应用并且返回该应用实例
    """
    # flask应用实例app的创建
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化app
    db.init_app(app)
    login_manager.init_app(app)

    # 将main python包注册为蓝本，用以视图函数等
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 返回该实例
    return app
