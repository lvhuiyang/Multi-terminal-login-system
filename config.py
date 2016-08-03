# -*- coding: utf-8 -*-
import os


class Config:
    """
    整个项目的配置类，用以配置多个环境，本项目只使用一个配置环境
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('MULTI_TERMINAL_DATABASE')
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass


config = {
    'default': Config
}
