# -*- coding: utf-8 -*-
from application.main import main
from application.models import User
from flask import (request, flash, redirect,
                   url_for, render_template, session)
from flask_login import (login_user, logout_user,
                         login_required, current_user)
from get_ip import get_ip_info
from redis import Redis

r = Redis(host='127.0.0.1', port=6379, db=0)


def get_device_info():
    ip = request.remote_addr
    platform = request.user_agent.platform
    browser = request.user_agent.browser
    return str(ip + ' , ' + platform + ' , ' + browser)


def my_login(user, device_info):
    """
    自己定义的用于管理session和redis的登录登出函数，使用跟随flask-login的登录登出函数
    """
    session[user] = user
    session[device_info] = device_info
    r.set(device_info, device_info)


def my_logout(user, device_info):
    session[user] = None
    session[device_info] = None
    r.delete(device_info)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        # 判断是否在/页面登陆后接着被其他终端下线的情况
        # 先判断用户flask-login是否登录，等待刷新，检测redis/session是否过期，若过期，则下线该终端
        if current_user.is_authenticated:
            on_line_flag = r.get(get_device_info())
            if on_line_flag is None:
                logout_user()
                flash(u"您的账号被其他终端下线，如需操作请重新登录")
                return redirect(url_for('main.index'))

        # 用户首次访问
        # 用户进行get请求访问时先获取用户IP以及设备的详细信息
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

    else:
        # 用户使用post请求进行登录，登陆成功redirect到首页，登录失败给出flash
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None and user.verify_password(password=request.form['password']):
            login_user(user=user)
            my_login(user=user.username, device_info=get_device_info())
            return redirect(url_for('main.index'))
        else:
            flash(u"账号或密码错误，请联系管理员")
            return redirect(url_for('main.index'))


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # GET请求用于使本终端下线
    if request.method == 'GET':
        my_logout(user=current_user.username, device_info=get_device_info())
        logout_user()
        flash(u"您已注销该账号，如有需要请重新登录")
        return redirect(url_for('main.index'))
    else:
        # POST请求用于下线其他终端
        device_info = request.form['hidden_form']
        my_logout(user=current_user.username, device_info=device_info)
        flash(u"您的账号被其他终端下线，如需操作请重新登录")
        return redirect(url_for('main.details'))


@main.route('/details', methods=['GET', 'POST'])
@login_required
def details():
    # 创建一个空列表准备显示所有终端的详细信息
    return_info = []
    # redis中变量值is None的时候代表该终端可能已经被下线，这时退出用户并重定向到主页
    on_line_flag = r.get(get_device_info())
    if on_line_flag is None:
        logout_user()
        return redirect(url_for('main.index'))
    # 遍历redis值找到所有设备的信息，并加入返回信息的数组，且在数组里找到此终端的位置
    for i in r.keys():
        return_info.append(i)

    # 设置一个标记的list
    number_list = []
    for i in range(0, len(return_info)):
        number_list.append(i)

    # 找到本终端所在list的位置
    local_int = return_info.index(get_device_info())
    return render_template("details.html", local_int=local_int, number_list=number_list, return_info=return_info)


@main.route('/clear')
@login_required
def clear():
    session.clear()
    r.flushdb()
    flash(u"您已经使所有终端下线，如需操作请重新登录")
    return redirect(url_for('main.index'))
