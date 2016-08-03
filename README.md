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
 
##  2.思路

+ 账号密码数据保存在mysql数据库中，登录请求时查询数据库验证账号密码是否正确。

+ 保存登录cookie，IP，设备信息，用以前端显示，并保存为log文件。

+ 登录的状态保存在redis中，用户对登录操作改变redis某值，redis值改变后结束对应回话，使对应终端上线/下线。

+ 必要使用ajax进行异步变化。

