# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import login_user, LoginManager, login_required, current_user
from flask import render_template, request, redirect, url_for
from forms import LogoutForm
from db import insert_db, select_db
from tools import print_time

legal_level = [15, 20, 45, 60, 100, 188, 226, 600, 360]


@login_required
def add():
    print_time()
    print "\nroot: add\n"
    form = LogoutForm()
    return render_template('add.html', form=form)


@login_required
def addlink():
    print_time()
    print "\nroot: addlink\n"
    link = request.args.get("link", "")
    level = int(request.args.get("level", "0"))
    uid = current_user.get_id()
    if level not in legal_level:
        return "红包档次输入错误"
    if check_link_exist(link):
        return "重复入库"
    res = insert_link_to_db(link, level, uid)
    if res:
        return "入库成功"
    else:
        return "入库失败"


#判断是否重复入库
def check_link_exist(link):
    sql = "select * from link where link='%s'" %link
    result = select_db(sql)
    if result:
        return True
    else:
        return False


# 入库操作
def insert_link_to_db(url, level, uid):
    sql = "insert into link(link,level,status,uid) values('%s',%d,1,'%s')" % (url, level, uid)
    return insert_db(sql)