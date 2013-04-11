import pymysql
import time

host = '172.16.18.254'
port = 3306
user = 'hdd_datauser'
passwd = 'oknej1984'
db = 'hdd_data'


def get_time():
    t = time.localtime()
    return '{0}-{1}-{2} / {3}:{4}:{5}'.format(t[0], str(t[1]).zfill(2), str(t[2]).zfill(2), str(t[3]).zfill(2), str(t[4]).zfill(2), str(t[5]).zfill(2),)


def get_settings():
    dic = dict()
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM itl_test_settings")
    d = cur.fetchall()
    cur.close()
    conn.close()
    for i in d:
        dic[i[0]] = i[1]
    return dic


def insert_warning(comp, operation, time, user_id, session_id):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("INSERT INTO itl_test_warnings(comp, operation, time, start_time, user_id, session_id) "
                "VALUES ('{0}','{1}','{2}','{3}', '{4}', '{5}') ".format(comp, operation, time, get_time(), user_id, session_id))
    cur.close()
    conn.close()