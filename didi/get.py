# -*- coding: utf-8 -*-
from datetime import datetime
from flask import request, render_template
from flask_login import current_user
from tools import get_level_status_by_id, get_phone_amount_by_id, get_uid_by_id
from tools import print_time


legal_level = [15, 20, 45, 60, 100, 188, 226, 600, 360]


def get():
    print_time()
    print "\nroot: get\n"
    s = request.args.get("id", "0")
    level, status = get_level_status_by_id(s)
    uid = get_uid_by_id(s)
    print "\n此id的level和status：", level, status, "\n"
    if level in legal_level:
        if status == 1:
            return render_template('get.html', id=s, level=level, uid=uid)
        else:
            phone, amount = get_phone_amount_by_id(s)
            return render_template('received.html', phone=phone, amount=amount)
    else:
        return u"非法链接"