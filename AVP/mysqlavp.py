import pymysql
import time

host='172.16.10.189'
port=3306
user='hdd_datauser'
passwd='oknej1984'
db='hdd_data'

def insert(club,comp,position,time):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("INSERT INTO avp(club,comp,{0}) VALUES ('{1}','{2}','{3}') ".format(position, club,comp,time))
    cur.close()
    conn.close()

def check_inbase(club,comp):

    """
    Check field in database. If field exist return 1, else return 0.
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT start FROM avp WHERE club={0} and comp = {1}".format(club, comp))
    d = cur.fetchall()
    cur.close()
    conn.close()
    if d == ():
        return 0
    else:
        return 1

def update(club,comp,position,time):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("UPDATE avp SET {0}='{1}' WHERE club={2} and comp = {3}".format(position,time,club,comp))
    cur.close()
    conn.close()