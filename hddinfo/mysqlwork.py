import pymysql

host='172.16.10.189'
port=3306
user='hdd_datauser'
passwd='oknej1984'
db='hdd_data'

def read_all_folders(club, comp):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT folder, size, accuracy, status, InRange FROM hdd_space WHERE comp = '{0}'AND club = '{1}' ".format(comp, club))
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d


def update_size(club,folder,size):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("UPDATE hdd_space SET Size={2} WHERE club={0} and comp=0 and folder='{1}'".format(club, folder, size))
    cur.close()
    conn.close()
def read(folder='pointblank', club='10'):

    """
    Return array in 2 elements.
    First - size
    Second - accuracy
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT size, accuracy FROM hdd_space WHERE Folder = '{0}' AND comp = '0' AND club = '{1}' ".format(folder, club))
    d = cur.fetchall()
    f = d[0]
    cur.close()
    conn.close()
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
    folder=folder.replace('\'','\\\'')
    cur.execute("SELECT size FROM hdd_space WHERE Folder = '{0}' AND comp = '0' AND club = '{1}' ".format(folder, club))
    d = cur.fetchall()
    cur.close()
    conn.close()
    if d == ():
        return 0
    else:
        return 1

def read_all_comp(club='10'):
    """
    Return array of all comp in database for this club
    """
    array=[]
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
    Return array of needs folders for this club
    """
    array=[]
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT folder FROM hdd_space WHERE club = '{0}' AND comp = 0 ".format(club))
    d = cur.fetchall()
    for i in d:
        array.extend(i)
    cur.close()
    conn.close()
    return array

def write_folder(folder, size, club, comp, status='0', InRange='1'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    folder=folder.replace('\'','\\\'')
    cur.execute("INSERT INTO hdd_space(Folder, Size, accuracy, Club, Comp, status, InRange) VALUES ('{0}','{1}','100','{2}','{3}', '{4}','{5}') ".format(folder,size,club,comp,status,InRange))
    cur.close()
    conn.close()

def del_folder(club, comp, folder):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("DELETE FROM hdd_space WHERE Club='{0}' AND Comp='{1}' AND Folder='{2}'".format(club, comp, folder))
    cur.close()
    conn.close()

