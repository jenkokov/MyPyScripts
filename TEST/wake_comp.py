# coding: utf8
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
import struct
import pymysql
mac = '00-16-17-EE-E4-94'
host='172.16.10.189'
port=3306
user='hdd_datauser'
passwd='oknej1984'
db='hdd_data'

def read_mac(club,comp):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT mac FROM hard_space WHERE comp = '{0}'AND club = '{1}' ".format(comp, club))
    d = cur.fetchall()
    cur.close()
    conn.close()
    return d[0][0]

def read_club(club):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    cur.execute("SELECT mac FROM hard_space WHERE club = '{0}' ".format(club))
    d = cur.fetchall()
    cur.close()
    conn.close()
    array=[]
    for i in d:
        array.extend(i)
    return array

def awake(mac):
    data = ''.join([struct.pack('6B', *[0xff] * 6),
                        struct.pack('96B', *[int(d, 16)
                                             for d in mac.split('-')] * 16)])
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    sock.sendto(data, ('<broadcast>', 9))
    sock.close()
    print 'Successful send packet to {0}'.format(mac)

def main():
    club=raw_input('Club: ')
    comp=raw_input('Comp: ')
    if comp =='0':
        mac_array=read_club(club)
        for mac in mac_array:
            awake(mac)
    else:
        mac = read_mac(club,comp)
        awake(mac)
        main()

if __name__ == '__main__':
    club='10'
    comp='1'
    main()