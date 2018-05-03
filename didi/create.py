# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, request
from flask_login import login_required, current_user
import uuid
from db import insert_db
from forms import LogoutForm
from tools import print_time


legal_level = [15, 20, 45, 60, 100, 188, 226, 600, 360]
vali_level = [188, 226, 600, 360]


@login_required
def create():
    print_time()
    print "\nroot: create\n"
    form = LogoutForm()
    return render_template('create.html', form=form)


@login_required
def createlink():
    print_time()
    print "\nroot: createlink\n"
    level = int(request.args.get("level", "0"))
    uid = current_user.get_id()
    if level not in legal_level:
        return "红包档次输入错误"
    res = insert_id_to_db(level, uid)
    if res and len(res) > 0:
        head = "http://toolazy.site/vali?id=" if level in vali_level else "http://toolazy.site/get?id="
        links = ""
        for s in res:
            links += str(level) + " : " + (head + s + '\n')
        return links
    else:
        return "链接生成错误"


def insert_id_to_db(level, uid):
    res = []
    for i in range(50):
        s = generate_id()
        sql = "insert into id(id,status,level,uid) values('%s',1,%d,'%s')" % (s, level, uid)
        if insert_db(sql):
            res.append(s)
    return res


def generate_id():
    s = str(uuid.uuid4())
    return s.replace('-', '')
