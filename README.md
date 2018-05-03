# TODO
验证码校验失败后不再继续
# 激活virtualenv
source venv/bin/activate

# uwsgi
    启动方式： 配置启动
    启动文件： /home/gaohongjie/didi/config.ini
    手动启动方式： uwsgi config.ini
# Supervisor：
    作用： 可以同时启动多个应用，当某个应用Crash的时候，他可以自动重启该应用，保证可用性。
    配置文件位置：/etc/supervisor/conf.d/my_flask_supervisor.conf
    启动服务 : sudo service supervisor start
    终止服务 : sudo service supervisor stop
# ngix:
    配置文件位置：/etc/nginx/sites-available/default
    重启服务： sudo service nginx start
    sudo service nginx stop
    sudo service nginx restart


# log:  
logs/uwsgi_supervisor.log

# start & stop
sudo service nginx stop
sudo service supervisor stop
sudo lsof -i:8001
sudo kill -9

uwsgi config.ini

sudo service supervisor start
sudo service nginx start


# /etc/supervisor/conf.d/my_flask_supervisor.conf:

[program:didi]
#启动命令入口
command=/root/development/venv/bin/uwsgi  /root/development/didi/config.ini

#命令程序所在目录
directory=/root/development/didi
#运行命令的用户名
#user=root

autostart=true
autorestart=true
#日志地址
stdout_logfile=/root/development/didi/logs/uwsgi_supervisor2.log

# /etc/nginx/sites-available/default:

server {
	  listen  80;
	  server_name toolazy.site; #公网地址

	  location / {
		include      uwsgi_params;
		uwsgi_pass   127.0.0.1:8002;  # 指向uwsgi 所应用的内部地址,所有请求将转发给uwsgi 处理
		uwsgi_param UWSGI_PYHOME /root/development/venv; # 指向虚拟环境目录
		uwsgi_param UWSGI_CHDIR  /root/development/didi; # 指向网站根目录
		uwsgi_param UWSGI_SCRIPT main:app; # 指定启动程序
	  }
	}
