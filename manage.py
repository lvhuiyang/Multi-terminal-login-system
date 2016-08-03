# -*- coding: utf-8 -*-
"""
该文件为整个项目的启动文件，包含shell和启动服务
"""
from application import create_app
from application import db
from application.models import User
from flask_script import Manager
from flask_script import Shell

app = create_app('default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
