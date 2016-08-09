# Multi-terminal-login-system
账号的多终端登录与管理系统


## 1.需求描述

### 请实现一个账号系统，能够进行多点登录的管理。

具体需求如下：
 
+ 用户可从多个设备或浏览器登录，分别会创建不同的会话；

+ 在一处登录后，可查看该用户当前所有在线会话；

+ 在一处登录后，可注销任一在线会话，被注销的会话需要重新登录，未被注销的会话不受影响；

+ 举例如下:
    
    用户通过 Chrome 和 Firefox 登录，分别标记为 会话1 和 会话2，登录后可以看到当前有两个在线会话。在 Firefox 中注销 会话1 后 Chrome 需要重新登录，Firefox 仍保持登录状态。
 
## 2.思路

+ 账号密码数据保存在mysql数据库中，登录请求时查询数据库验证账号密码是否正确。

+ flask-login用以控制当前终端的登录状态,使用redis控制其他终端。

+ 登录的设备信息保存在session和redis中，用户对登录登出操作使redis值改变后刷新页面对应操作，使对应终端上线/下线。具体:

+ 必要使用ajax进行异步变化。（暂时未实现）

## 3.总结

+ flask自带的session是保存在客户端cookie中的，这种session机制叫做 `client-side session` ,主要操作的是本终端的session，需要操作其他终端的session的话需要使用 redis劫持，也就是对应的 `server-side session`.

+ 目前使用flask-login控制本终端和登录状态， redis 用以控制其他终端。

## 4.安装与使用

+ 系统环境:

    > mysql

    > redis

    > git

    > 系统环境变量 SECRET_KEY 用以存储密钥

    > 系统环境变量 MULTI_TERMINAL_DATABASE 用以存储对应mysql的地址

+ clone本仓库地址,对应命令：

```bash
git clone git@github.com:lvhuiyang/Multi-terminal-login-system.git
```

+ 创建虚拟环境并且安装依赖

```bash
# 安装虚拟环境
virtualenv venv

# 使用当前虚拟环境
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 升级setuptools
pip install --upgrade setuptools

# 安装对应依赖
pip install -r requirements.txt
```

+ 使用gunicorn启动服务

```
gunicorn -w4 -b0.0.0.0:8000 manage:app
```


## 5.实例展示

### 安卓终端

![android](http://obmfmt907.bkt.clouddn.com/andriod_demo.jpg)

### linux终端

![linux_chrome2](http://obmfmt907.bkt.clouddn.com/Screenshot%20from%202016-08-09%2010:53:39.png)

![linux_chrome1](http://obmfmt907.bkt.clouddn.com/Screenshot%20from%202016-08-09%2010:54:02.png)

### windows终端

![windows](http://obmfmt907.bkt.clouddn.com/QQ%E6%88%AA%E5%9B%BE20160809104305.jpg)


