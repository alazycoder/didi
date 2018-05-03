# -*- coding: utf-8 -*-
from datetime import datetime
from flask import request, render_template
from flask_login import current_user
from db import select_db
from tools import get_level_status_by_id, get_html_by_requests, get_phone_amount_by_id, get_uid_by_id
from tools import print_time

legal_level = [15, 20, 45, 60, 100, 188, 226, 600, 360]


def vali():
    print_time()
    print "\nroot: vali\n"
    s = request.args.get("id", "0")
    level, status = get_level_status_by_id(s)
    uid = get_uid_by_id(s)
    print "\n此id的level和status", level, status, "\n"
    if level in legal_level:
        if status == 1:
            return render_template('vali.html', id=s, level=level, uid=uid)
        else:
            phone, amount = get_phone_amount_by_id(s)
            return render_template('received.html', phone=phone, amount=amount)
    else:
        return u"非法链接"


def getvalicode():
    print_time()
    print "\nroot: getvalicode\n"
    phone = request.args.get("phone")
    res = get_vali_code(phone)
    return res


# 给该手机发验证码
def get_vali_code(phone):
    print_time()
    print "in get_vali_code"
    url = "https://hongbao.xiaojukeji.com/hongbao/send/code?phone=" + phone
    res = get_html_by_requests(url)
    if res.find("10000") != -1:
        return "已发送"
    elif res.find("30003") != -1:  # 1分钟只能接受一次验证码
        return "请稍后刷新重试"
    else:                          # 每天最多发5条短信
        return "今日次数达上限"