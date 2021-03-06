import pymysql
import time
import os
import logging

general_log = 'C:\\dslogon\\general.log'
if not os.path.exists('C:\\dslogon\\'):
    os.makedirs('C:\\dslogon\\')
    f = open(general_log, 'a')
    f.close()
logging.basicConfig(filename=general_log, level=logging.INFO,
                    format='%(asctime)s: [mysqlwork.py] [%(levelname)s] %(message)s')


host = '172.16.10.189'
port = 3306
user = 'hdd_datauser'
passwd = 'oknej1984'
db = 'hdd_data'


def get_ideals():
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT club, folder, size FROM hdd_space WHERE comp = 0")
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d


def get_datetime(val='datetime'):
    t = time.localtime()
    if val == 'datetime':
        return '{0}-{1}-{2} {3}:{4}:{5}'.format(t[0], str(t[1]).zfill(2), str(t[2]).zfill(2), str(t[3]).zfill(2),
                                                str(t[4]).zfill(2), str(t[5]).zfill(2))
    if val == 'date':
        return '{0}-{1}-{2}'.format(t[0], str(t[1]).zfill(2), str(t[2]).zfill(2))
    if val == 'time':
        return '{0}:{1}:{2}'.format(str(t[3]).zfill(2), str(t[4]).zfill(2), str(t[5]).zfill(2))

needContinue = True
count = 0
while needContinue:
    try:

        needContinue = False
    except:
        count += 1
        if count < 6:
            print 'Error to connect to DB! Try {0} of 5. Retry after 20 second... '.format(count)
            time.sleep(15)
            needContinue = True
        else:
            needContinue = False
            logging.error('Can not connect to DB on host {0}'.format(host))


def read_all_folders(club, comp):
    needContinue = True
    count = 0
    d = []
    while needContinue:
        try:
            conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
            cur = conn.cursor()
            cur.execute("SELECT folder, size, accuracy, status, InRange,time FROM hdd_space "
                        "WHERE comp = '{0}'AND club = '{1}' ".format(comp, club))
            d = cur.fetchall()
            cur.close()
            conn.close()
            needContinue = False

        except:
            count += 1
            if count < 6:
                print 'Error to connect to DB! Try {0} of 5. Retry after 20 second... '.format(count)
                time.sleep(15)
                needContinue = True
            else:
                needContinue = False
                logging.error('Can not connect to DB on host {0}'.format(host))
                d = ()
    return d


def update_size(club, folder, size):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("UPDATE hdd_space SET Size={2}, sync_status = '0' WHERE club={0} and comp=0 and folder='{1}'".format(club, folder, size))
    cur.close()
    conn.close()


def read(folder='pointblank', club='10'):

    """
    Return array in 2 elements.
    First - size
    Second - accuracy
    """

    needContinue = True
    count = 0
    f = 0
    while needContinue:
        try:
            conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
            cur = conn.cursor()
            cur.execute("SELECT size, accuracy FROM hdd_space WHERE Folder = '{0}' AND comp = '0' AND club = '{1}' ".format(folder, club))
            d = cur.fetchall()
            f = d[0]
            cur.close()
            conn.close()
            needContinue = False
        except:
            count += 1
            if count < 6:
                print 'Error to connect to DB! Try {0} of 5. Retry after 20 second... '.format(count)
                time.sleep(15)
                needContinue = True
            else:
                needContinue = False
                logging.error('Can not connect to DB on host {0}'.format(host))
                f = ()

    return f


def drop_comp(club='10', comp='108'):

    """
    Delete all fields with this comp
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("DELETE FROM `hdd_space` WHERE Club='{0}' AND Comp='{1}' ".format(club, comp))
    cur.close()
    conn.close()


def check_inbase(folder='hon1', club='10'):

    """
    Check field in database. If field exist return 1, else return 0.
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    folder = folder.replace('\'', '\\\'')
    cur.execute("SELECT size FROM hdd_space WHERE Folder = '{0}' AND comp = '0' AND club = '{1}' ".format(folder, club))
    d = cur.fetchall()
    cur.close()
    conn.close()
    if d == ():
        return 0
    else:
        return 1


def read_folders(club):

    """
    return dict of all folders needs for this club
    """
    array = {}
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT folder,size,accuracy FROM hdd_space WHERE comp = '0' AND club = '{0}' ".format(club))
    d = cur.fetchall()
    cur.close()
    conn.close()
    for i in d:
            array[i[0]] = [i[1], i[2]]
    return array


def read_all_comp(club='10'):
    """
    Return array of all comp in database for this club
    """
    array = []
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT comp FROM hdd_space WHERE club = '{0}'".format(club))
    d = cur.fetchall()
    for i in d:
        if i[0] not in array:
            array.extend(i)
    cur.close()
    conn.close()
    return array


def read_needsfolder(club='10'):

    """
    Return array of needs folders and his size for this club
    """
    array = {}
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT folder,size FROM hdd_space WHERE club = '{0}' AND comp = 0 ".format(club))
    d = cur.fetchall()
    for i in d:
        array[i[0]] = i[1]
    cur.close()
    conn.close()
    return array


def write_folder(folder, size, club, comp, status='0', InRange='1'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    folder = folder.replace('\'', '\\\'')
    cur.execute("INSERT INTO hdd_space(Folder, Size, accuracy, Club, Comp, status, InRange, sync_status) "
                "VALUES ('{0}','{1}','500','{2}','{3}', '{4}','{5}','0') ".format(folder, size, club, comp, status, InRange))
    cur.close()
    conn.close()


def write_mass(array):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    values = 'INSERT INTO hdd_space(Folder, Size, accuracy, Club, Comp, status, InRange, sync_status, time) VALUES '
    for i in array:
        values = values + '(\'' +\
                 str(i[0].replace('\'', '\\\'')) + '\',\'' + \
                 str(i[1]) + \
                 '\',\'500\',\'' + \
                 str(i[2]) + '\',\'' + \
                 str(i[3]) + '\',\'' + \
                 str(i[4]) + '\',\'' + \
                 str(i[5]) + \
                 '\',\'0\',\'' + \
                 str(get_datetime()) + '\'),'
    values = values[0:-1]
    cur.execute(values)
    cur.close()
    conn.close()


def del_folder(club, comp, folder):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("DELETE FROM hdd_space WHERE Club='{0}' AND Comp='{1}' AND Folder='{2}'".format(club, comp, folder))
    cur.close()
    conn.close()

if __name__ == "__main__":
    print 'System file! Can\'t run!'