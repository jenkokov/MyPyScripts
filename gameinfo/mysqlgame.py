import pymysql

host='172.16.10.189'
port=3306
user='hdd_datauser'
passwd='oknej1984'
db='hdd_data'

def create_game(game,exepath,method,ActualVerison):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    if check_inbase(game)==0:
        cur.execute("INSERT INTO game_info(game,EXEpath,Method,ActualVersion) VALUES ('{0}','{1}',{2},'{3}') ".format(game,exepath,method,ActualVerison))
    else:
        cur.execute("UPDATE game_info SET ActualVersion='{1}', EXEpath='{2}' WHERE game = '{0}'".format(game,ActualVerison,exepath))
    cur.close()
    conn.close()

def games_version(club):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT game, EXEpath, method, ActualVersion FROM game_info WHERE InClub{0} = 1".format(club))
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d

def check_inbase(game):

    """
    Check field in database. If field exist return 1, else return 0.
    """
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT ActualVersion FROM game_info WHERE game = '{0}'".format(game))
    d = cur.fetchall()
    cur.close()
    conn.close()
    if d == ():
        return 0
    else:
        return 1

#create_game(20,'WoT','D:\Games\WoT\WorldOfTanks.exe',1,'0.7.6')
games_version(20)