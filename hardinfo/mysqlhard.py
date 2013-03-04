import pymysql

host = '172.16.18.254'
port = 3306
user = 'hdd_datauser'
passwd = 'oknej1984'
db = 'hdd_data'


def insert_data(club, comp, param, value):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT os FROM hard_space WHERE club={0} and comp = {1}".format(club, comp))
    d = cur.fetchall()
    if d == ():
        cur.execute("INSERT INTO hard_space(club,comp,{0},sync_status) VALUES ('{1}','{2}','{3}','0') ".format(param, club, comp, value))
    else:
        cur.execute("UPDATE hard_space SET {2}='{3}', sync_status = '0' WHERE club={0} and comp = {1}".format(club, comp, param, value))
    cur.close()
    conn.close()


def get_free_space():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT club, comp, diskD, time FROM hard_space ORDER BY club, comp")
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d


def check_in_base(club, comp):

    """
    Check field in database. If field exist return 1, else return 0.
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT os FROM hard_space WHERE club={0} and comp = {1}".format(club, comp))
    d = cur.fetchall()
    cur.close()
    conn.close()
    if d == ():
        return 0
    else:
        return 1