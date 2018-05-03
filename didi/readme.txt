待做：
    验证码校验失败后不再继续

source venv/bin/activate

uwsgi
    启动方式： 配置启动
    启动文件： /home/gaohongjie/didi/config.ini
    手动启动方式： uwsgi config.ini
Supervisor：
    作用： 可以同时启动多个应用，当某个应用Crash的时候，他可以自动重启该应用，保证可用性。
    配置文件位置：/etc/supervisor/conf.d/my_flask_supervisor.conf
    启动服务 : sudo service supervisor start
    终止服务 : sudo service supervisor stop
ngix:
    配置文件位置：/etc/nginx/sites-available/default
    重启服务： sudo service nginx start
    sudo service nginx stop
    sudo service nginx restart


log:  logs/uwsgi_supervisor.log

source venv/bin/activate

sudo service nginx stop
sudo service supervisor stop
sudo lsof -i:8001
sudo kill -9

uwsgi config.ini

sudo service supervisor start
sudo service nginx start



注意问题：
1： 入库失败大部分原因是此链接重复入库
2： 同一个用户接受多个验证码的时间间隔应该大于1分钟

