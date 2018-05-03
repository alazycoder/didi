# -*- coding: utf-8 -*-
from flask import request, render_template
from datetime import datetime, timedelta
from flask_login import login_required, current_user
import operator
import json
from db import select_db
from forms import LogoutForm


def ad():
    return render_template('ad.html')


@login_required
def monitor():
    print "\nroot: monitor\n"
    form = LogoutForm()
    return render_template('monitor.html', form=form)


@login_required
def echarts():
    uid = current_user.get_id()
    name24, value24 = get_hour_data(h=24, uid=uid)
    name7, value7 = get_day_data(d=7, uid=uid)
    name30, value30 = get_day_data(d=30, uid=uid)
    data = {
        "name24": name24,
        "value24": value24,
        "name7": name7,
        "value7": value7,
        "name30": name30,
        "value30": value30,
    }
    return json.dumps(data)


def get_hour_data(h=24, uid=""):
    now = datetime.today()
    ed = datetime(now.year, now.month, now.day, now.hour) + timedelta(hours=1)
    st = ed - timedelta(hours=h)
    res = get_data(st, ed, uid=uid)
    count = {}
    for i in range(h):
        k = st + timedelta(hours=i)
        count[k] = 0
    for item in res:
        k = item[0]
        t = datetime(k.year, k.month, k.day, k.hour)
        count[t] = count.get(t, 0) + 1
    sorted_count = sorted(count.items(), key=operator.itemgetter(0))
    name = []
    value = []
    for item in sorted_count:
        name.append(item[0].strftime("%H") + ":00")
        value.append(item[1])
    return name, value


def get_day_data(d=7, uid=""):
    now = datetime.today()
    ed = datetime(now.year, now.month, now.day) + timedelta(days=1)
    st = ed - timedelta(days=d)
    res = get_data(st, ed, uid=uid)
    count = {}
    for i in range(d):
        k = st + timedelta(days=i)
        count[k] = 0
    for item in res:
        k = item[0]
        t = datetime(k.year, k.month, k.day)
        count[t] = count.get(t, 0) + 1
    sorted_count = sorted(count.items(), key=operator.itemgetter(0))
    name = []
    value = []
    for item in sorted_count:
        name.append(item[0].strftime("%m-%d"))
        value.append(item[1])
    return name, value


def get_data(st, ed, uid=""):
    sql = "select create_time from record where create_time>='%s' and create_time<'%s' and uid='%s'" % (st, ed, uid)
    res = select_db(sql)
    return res
