from datetime import datetime
import MySQLdb
import traceback

host = "47.104.70.171"
user_name = "root"
pass_word = "032610"
datebase = "didi"
port = 3306


def insert_db(sql):
    res = True
    db = MySQLdb.connect(host=host,user=user_name, passwd=pass_word, db=datebase, port=port)
    cursor = db.cursor()
    print "sql= ", sql
    try:
        cursor.execute(sql)
        db.commit()
        print "insert_db successd"
    except:
        res = False
        traceback.print_exc()
        db.rollback()
        print "insert_db failed"
    db.close()
    return res


def update_db(sql):
    res = True
    db = MySQLdb.connect(host=host,user=user_name, passwd=pass_word, db=datebase, port=port)
    cursor = db.cursor()
    print "sql= ", sql
    try:
        cursor.execute(sql)
        db.commit()
        print "update_db succeed"
    except:
        res = False
        traceback.print_exc()
        db.rollback()
        print "update_db failed"
    db.close()
    return res


def select_db(sql):
    results = []
    db = MySQLdb.connect(host=host,user=user_name, passwd=pass_word, db=datebase, port=port)
    cursor = db.cursor()
    print "sql= ", sql
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print "select_db succeed"
        print "resultes: ", results
    except:
        traceback.print_exc()
        print "select_db failed"
    db.close
    return results
