# -*- coding: utf-8 -*-
from application.main import main
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_user
from get_ip import get_ip_info
from application.models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        """
        用户进行get请求访问时先获取用户IP以及设备的详细信息
        """
        request_ip = request.remote_addr
        request_area = get_ip_info(request_ip)
        request_platform = request.user_agent.platform
        request_browser = request.user_agent.browser
        request_info = {
            'request_ip': request_ip,
            'request_area': request_area,
            'request_platform': request_platform,
            'request_browser': request_browser
        }
        return render_template('index.html', request_info=request_info)

    elif request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None and user.verify_password(password=request.form['password']):
            login_user(user=user)
            return redirect(url_for('main.index'))
        else:
            flash(u"账号或密码错误，请联系管理员")
            return redirect(url_for('main.index'))
    else:
        u"请求非法"


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    else:
        u"请求非法"
