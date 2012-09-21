import pymysql
import time

host='172.16.10.189'
port=3306
user='hdd_datauser'
passwd='oknej1984'
db='hdd_data'

def insert(club,comp,position,time,status):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("INSERT INTO avp(club,comp,{0},status,sync_status) VALUES ('{1}','{2}','{3}','{4}','0') ".format(position, club,comp,time,status))
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

def check_torrent(club,comp,torrent):
    """
    Check field in database. If field exist return 1, else return 0.
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT time FROM utorrent WHERE club={0} and comp = {1} and torrent='{2}'".format(club, comp,torrent))
    d = cur.fetchall()
    cur.close()
    conn.close()
    if d == ():
        return 0
    else:
        return 1

def insert_torrent(club,comp,torrent,date,time,status):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("INSERT INTO utorrent (club,comp,torrent,status,time,date) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(club,comp,torrent,status,time,date))
    cur.close()
    conn.close()

def update_torrent(club,comp,torrent,date,time,status):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("UPDATE utorrent SET time='{0}', status='{1}', date = '{5}' WHERE club={2} and comp = {3} and torrent = '{4}'".format(time,status,club,comp,torrent,date))
    cur.close()
    conn.close()

def update(club,comp,position,time,status):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("UPDATE avp SET {0}='{1}', status = '{4}', sync_status = '0' WHERE club={2} and comp = {3}".format(position,time,club,comp,status))
    cur.close()
    conn.close()

def select_club(club, sorting):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute('SELECT * FROM avp WHERE club={0} order by {1}'.format(club,sorting))
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d

def select_torrent(club,sdate,fdate):

    """
    Select torrent betwen sdate to fdate.
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT comp,date,time,torrent,status FROM utorrent where club={0} and date >= '{1}' and date <= '{2}' order by torrent,comp".format(club,sdate,fdate))
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d

def get_comp(table,club,sdate,fdate):
    """
    Select all comp for club in table.
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT comp FROM {0} WHERE club='{1}' and date >= '{2}' and date <= '{3}'".format(table,club,sdate,fdate))
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d


def check_comp(club,sdate,fdate):
    comps = []
    ncomps = []
    all_comps = get_comp('utorrent',club,sdate,fdate)
    compcount=0
    if club == '10':
        compcount = range(1,98)
    if club == '11':
        compcount = range(1,54)
    if club == '12':
        compcount = range(1,81)
    if club == '20':
        compcount = range(1,88)
    for i in sorted(all_comps):
        if i[0] not in comps:
            comps.append(i[0])
    for i in compcount:
        if i not in comps:
            ncomps.append(i)
    return ncomps