# -*- coding: utf-8 -*-
import os
import comparegames
import pymysql
import mysqlwork
import socket
import sys


def delfolder(folder):
    mysqlwork.del_folder(club, comp, folder)
    print 'Папка \'{0}\' удалена в клубе #{1}'.format(folder, club)


def add_new_folder(folder):
    if not os.path.exists(u'D:/Games/' + folder):
        print 'Папка {0} не найдена!'.format(folder)
        return
    size = comparegames.get_size(u'D:/Games/' + folder)
    if mysqlwork.check_inbase(folder, club) == 1:
        mysqlwork.update_size(club, folder, size)
        print 'Папка {0} для клуба #{1} обновлена!'.format(folder.upper(), club)
    else:
        mysqlwork.write_folder(folder.lower(), size, club, comp, 1, 1)
        print 'Папка {0} для клуба #{1} добавлена!'.format(folder.upper(), club)


def write2sql():
    mysqlwork.drop_comp(club, '0')
    d_dict = os.listdir('D:/Games')
    conn = pymysql.connect(host='172.16.10.189', port=3306, user='hdd_datauser', passwd='oknej1984', db='hdd_data')
    cur = conn.cursor()
    for word in d_dict:
        word = word.lower()
        print 'Подсчет размера и запись в базу ' + u'D:/Games/' + word
        size = comparegames.get_size(u'D:/Games/' + word)
        cur.execute("INSERT INTO hdd_space(Folder, Size, accuracy, Club, Comp, Status,InRange) "
                    "VALUES ('{0}','{1}',100,'{2}', '{3}',1,1)".format(word, size, club, comp))
        #cur.execute("UPDATE hdd_space SET Folder='{0}' WHERE 1".format(word))
    cur.close()
    conn.close()

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    comp = '0'
    club = raw_input('ID клуба (оставить пустым для использования этого клуба): ')
    if club == '':
        club = ip.split('.')[2]
    ques = raw_input('Удалить? (\'Y\' для удаления): ')
    if ques == 'y' or ques == 'Y':
        dfolder = raw_input('Введите папку для УДАЛЕНИЯ: ')
        delfolder(dfolder.lower())
        sys.exit()
    nfolder = raw_input('Новая папка D:\\Games (для обновления всех папок введите \'NEW\'): ')
    if nfolder == 'NEW':
        write2sql()
    else:
        add_new_folder(nfolder.lower())