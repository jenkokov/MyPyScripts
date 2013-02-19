# -*- coding: utf-8 -*-
import sys
import mysqlwork
import datetime
import logging
import os

general_log = 'C:\\dslogon\\general.log'
if not os.path.exists(general_log):
    os.makedirs('C:\\dslogon')
    f = open(general_log, 'a')
    f.close()
logging.basicConfig(filename=general_log, level=logging.INFO,
                    format='%(asctime)s: [showgames.py] [%(levelname)s] %(message)s')

mysql_count = 0


class Folder ():
    def __init__(self, size, accuracy, status, InRange, time):
        self.size = size
        self.accuracy = accuracy
        self.status = status
        self.InRange = InRange
        self.time = time

    def __repr__(self):
        f = [self.size, self.accuracy, self.status, self.InRange]
        return f


def main(club, comp):
    global mysql_count
    all_comp = mysqlwork.read_all_comp(club)
    mysql_count += 1
    if int(comp) not in all_comp:
        print 'Comp #{0} or club #{1} not in base!'.format(comp, club)
        return
    array = mysqlwork.read_all_folders(club, comp)
    mysql_count += 1
    for i in array:
        d[i[0]] = Folder(i[1], i[2], i[3], i[4], i[5])
    needs_folder = mysqlwork.read_needsfolder(club)
    mysql_count += 1
    print '\n+'.ljust(75, '-') + '+\n' + '|' + 'Name'.center(25) + '|' + 'Size'.center(11) + '|' + 'Ideal'.center(11) +\
          '|Difference'.ljust(12) + '|' + 'Status'.center(11) + '|' + '\n' + '+'.ljust(74, '-') + '+'
    for name in needs_folder:
        if name not in d:
            ideal_size = mysqlwork.read(name, club)
            mysql_count += 1
            print '|' + name[:25].ljust(25) + '| no data'.ljust(12) + '| ' + str(ideal_size[0]).ljust(10) + '| ' +\
                  str(ideal_size[0]).ljust(10) + '| NO EXISTS!|'
    for name in sorted(d):
        status = 'Need'
        if name not in needs_folder:
            status = 'NO NEED!'
            print '|' + name[:25].ljust(25) + '| ' + str(d[name].size).ljust(10) + '| NO DATA!'.ljust(12) + '| ' +\
                  str(d[name].size).ljust(10) + '| ' + status.ljust(10) + '|'
        else:
            ideal_size = mysqlwork.read(name, club)
            mysql_count += 1
            print '|' + name[:25].ljust(25) + '| ' + str(d[name].size).ljust(10) + '| ' + str(ideal_size[0]).ljust(10) +\
                  '| ' + str(abs(d[name].size - ideal_size[0])).ljust(10) + '| ' + status.ljust(10) + '|'
    print '+'.ljust(74, '-') + '+\n'


def info_club(club):
    global mysql_count
    all_comp = mysqlwork.read_all_comp(club)
    mysql_count += 1
    if len(all_comp) == 0:
        print 'Club #{0} not in base!'.format(club)
        return
    needs_folder = mysqlwork.read_needsfolder(club)
    mysql_count += 1
    f = open('D:/log/Log_for_Club{0}.txt'.format(club), 'w')
    time = datetime.datetime.now()
    f.write('Time: ' + str(time) + '\n\n')
    all_comp.sort()
    for machine in all_comp:
        d = {}
        out_of_range = []
        not_exist = []
        not_need = []
        array = mysqlwork.read_all_folders(club, machine)
        mysql_count += 1
        for i in array:
            d[i[0]] = Folder(i[1], i[2], i[3], i[4], i[5])
        for name in d:
            if d[name].InRange == 0:
                out_of_range.append(name)
        for name in needs_folder:
            if name not in d:
                not_exist.append(name)
        for name in d:
            if name not in needs_folder:
                not_need.append(name)
        if len(out_of_range) != 0 or len(not_exist) != 0 or len(not_need) != 0:
            try:
                date = d[out_of_range[0]].time
            except:
                date = d[not_exist[0]].time
            print '\nErrors on {0} comp (last scan at {1}):'.format(machine, date)
            f.write('\nErrors on {0} comp (last scat at {1}):\n'.format(machine, date))
            j = 1
            out_of_range.sort()
            not_exist.sort()
            not_need.sort()
            for i in not_exist:
                print '\t{1}. NO EXISTS folder {0}'.format(i.upper(), j).ljust(45, '.') + ' <NONE>'
                f.write('\t{1}. NO EXISTS {0}'.format(i.upper(), j).ljust(45, '.') + ' <NONE>\n')
                j += 1
            for i in not_need:
                print '\t{1}. NO NEED folder {0}'.format(i.upper(), j).ljust(45, '.') + ' ' + str(d[i].size) + ' MB'
                f.write('\t{1}. NO NEED folder {0}'.format(i.upper(), j).ljust(45, '.') + ' ' + str(d[i].size) + ' MB\n')
                j += 1
            for i in out_of_range:
                if i in needs_folder:
                    ideal_size = needs_folder[i]
                    delta_size = abs(d[i].size - ideal_size)
                    print '\t{1}. OUT OF RANGE folder {0}'.format(i.upper(), j).ljust(45, '.') + ' {0} MB'.format(delta_size)
                    f.write('\t{1}. OUT OF RANGE folder {0}'.format(i.upper(), j).ljust(45, '.') + ' {0} MB\n'.format(delta_size))
                    j += 1

    f.close()

if __name__ == '__main__':
    d = {}
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 2:
        info_club(sys.argv[1])
    print 'Total count of MySQL operation: ', mysql_count
    sys.exit()