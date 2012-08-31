import pymysql

host='172.16.10.189'
port=3306
user='hdd_datauser'
passwd='oknej1984'
db='hdd_data'

def get_comp(table,club):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT comp FROM {0} WHERE club='{1}'".format(table,club))
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d

def main():
    table=raw_input('Table for show: ')
    club=raw_input('Input ID club: ')
    all_comps = get_comp(table,club)
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
    print 'Comps for club #{0} IN TABLE \'{1}\':'.format(club,table)
    string=''
    for comp in comps:
        string = string + str(comp) + ', '
    print string[:-2]+'.'
    print 'Comps for club #{0} NOT IN TABLE \'{1}\':'.format(club,table)
    string=''
    for comp in ncomps:
        string = string + str(comp) + ', '
    print string[:-2]+'.'



if __name__=='__main__':
    comps=[]
    ncomps=[]
    main()