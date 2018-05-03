# -*- coding: utf-8 -*-
from flask import render_template, request
import requests
from datetime import datetime
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from db import insert_db, update_db, select_db


def get_html_by_requests(url):
    print_time()
    print "in get_html_by_requests : ", url
    try:
        r = requests.get(url, timeout=30)  # 设置timeout
        r.raise_for_status()  # 如果状态不是200(ok)，引发HTTPError异常
        r.encoding = r.apparent_encoding
        print "get_html_by_requests succeed"
        print r.content
        return r.content
    except:
        traceback.print_exc()
        print "get_html_by_requests failed"
        return "error"


def get_html_by_phantomjs(url):
    print_time()
    print "in get_html_by_phantomjs : ", url
    try:
        driver = webdriver.PhantomJS()
        driver.get(url)
        print "get_html_by_phantomjs succeed"
        return driver.page_source
    except:
        traceback.print_exc()
        print "get_html_by_phantomjs failed"
        return "error"


def get_soup(url):
    page_source = get_html_by_phantomjs(url)
    soup = BeautifulSoup(page_source, "html.parser")
    return soup


def get_url_by_level_uid(level, uid):
    urls = []
    sql = "select link from link where level=%d and status=1 and uid='%s'" % (level, uid)
    results = select_db(sql)
    if len(results) > 0:
        for item in results:
            urls.append(item[0])
    return urls


def update_status_by_link(link):
    sql = "update link set status=0,modify_time='%s' where link='%s'" % (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), link)
    update_db(sql)


def update_status_by_id(id):
    sql = "update id set status=0,modify_time='%s' where id='%s'" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id)
    update_db(sql)


def update_count_by_link(link):
    sql = "update link set get_count=get_count+1 where link='%s'" % (link)
    update_db(sql)


def get_uuid_and_sign_from_url(url):
    print_time()
    print "get_uuid_and_sign_from_url: ", url
    if url.find("hongbao.xiaojukeji.com") == -1:
        return False, None, None
    soup = get_soup(url)
    if soup.text.find(u"滴滴红包") == -1:
        return False, None, None
    if soup.find("div", {"class": "channel"}):
        return False, None, None
    text = soup.find_all("script")[-1].text
    data = text.split('\n')[2]
    data = eval(data[15:-1])
    return True, data["uuid"], data["sign"]


def get_rid_from_url(url):
    index = url.find("rid")
    return str(url[index + 4:index + 11])


def get_packet(uuid, sign, rid, phone, code):
    print_time()
    url = "https://hongbao.xiaojukeji.com/hongbao/receive?rid=" + rid + "&phone=" + phone + "&uuid=" + uuid + "&sign=" + sign
    if len(code) == 4:
        url += "&code=" + code
    res = get_html_by_requests(url)
    try:
        res = eval(res)
        if res.get("code") == 10000:
            return res.get("data", {}).get("batchInfo", {}).get("amount")
    except:
        print "eval res failed"
        print res
    return 0  # 领取失败


def get_links_by_phone(num):
    links = []
    num = int(num)
    sql = "select link from record where phone=%d " % num
    results = select_db(sql)
    if len(results) > 0:
        for item in results:
            links.append(item[0])
    return links


def get_phone_amount_by_id(s):
    sql = "select phone,amount from record where id='%s'" % s
    results = select_db(sql)
    if results and len(results)>0:
        return results[0][0], results[0][1]
    return None, 5  # 查询无果默认手机号None 已领取5元



def update_record_to_db(phone, link, id, uid, amount):
    phone = int(phone)
    sql = "insert into record(phone,link,id,uid,amount) values(%d,'%s','%s','%s',%d)" % (phone, link, id, uid, amount)
    insert_db(sql)


def pay(s, level, phone, code, uid):
    print_time()
    _, status = get_level_status_by_id(s)
    if status !=1:
	return 0
    urls = get_url_by_level_uid(level, uid)  # 获取当前可用links
    print "urls: ", urls
    used_links = get_links_by_phone(phone)  # 获取当前手机号已领取的links
    print "used_links: ", used_links
    for url in urls:
        if url in used_links:  # 已领取的链接不在继续领取
            continue
        can_use, uuid, sign = get_uuid_and_sign_from_url(url)
        print url, can_use, uuid, sign
        if can_use:
            rid = get_rid_from_url(url)
            amount = get_packet(uuid, sign, rid, phone, code)
            # amount > 0 领取成功  0 领取失败 -1 库存不足
            if amount and amount > 0:
                update_status_by_id(s)  # 标记此链接失效
                update_count_by_link(url)  # 链接使用次数加1
                update_record_to_db(phone, url, s, uid, amount)  # 添加购买记录
                return amount
        else:
            update_status_by_link(url)  # 标记为已经用完的链接
    return -1  # 库存不足


# 在id表中查level和status
def get_level_status_by_id(s):
    sql = "select level,status from id where id='%s'" % s
    results = select_db(sql)
    if len(results) == 1:
        return results[0][0], results[0][1]
    return None, None


def get_uid_by_id(s):
    sql = "select uid from id where id ='%s'" % s
    results = select_db(sql)
    if len(results) == 1:
        return results[0][0]
    return None


def getpacket():
    print_time()
    print "\nroot: getpacket\n"
    s = request.args.get("id")
    level = int(request.args.get("level"))
    phone = request.args.get("phone")
    code = request.args.get("code", "0")
    uid = request.args.get("uid", "0")
    if s and level and phone:
        print s, level, phone, code, uid
        count = pay(s, level, phone, code, uid)
        print "\ncount:", count, "\n"
        return str(count)
    else:
        return "-2"


def received():
    print_time()
    print "\nroot: received\n"
    s = request.args.get("id")
    phone, amount = get_phone_amount_by_id(s)
    return render_template('received.html', phone=phone, amount=amount)


def print_time():
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S")
