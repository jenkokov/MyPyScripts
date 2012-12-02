import sys
import os
import datetime
import shutil
import time
import mysqlwork
import socket
import restore_game

mysql_count = 0
out_of_range=[]
logfile_name = 'D:\log\Dlog.txt'

def write_log(string):
    f = open(logfile_name, 'a')
    print string
    f.write(string+'\n')
    f.close()

def check_size(f_size, accuracy, r_size):
    if abs(int(f_size)-int(r_size)) > int(accuracy):
        return ['Out of range to: ' + str(abs(int(f_size)-int(r_size))-int(accuracy)) + ' MB',0]
    else:
        return ['Normal size!',1]


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except:
                continue
    return str(total_size/1024/1024)

def delfolder(array):
    global mysql_count
    write_log('Start deleting folders...\n\n')
    for i in array:
        if os.path.isdir('D:/Games/'+ i) == 1:
            #shutil.rmtree('D:/Games/'+ i, 1)
            pass
        else:
            #os.remove("D:/Games/"+ i)
            pass
        mysqlwork.del_folder(club,comp,i)
        mysql_count += 1

def formatprint(string, massive=[]):
    global out_of_range
    global mysql_count
    mass_to_mysql=[]
    f = open(logfile_name, 'a')
    print string
    f.write(string + '\n')
    if massive <> []:
        inbase = mysqlwork.read_folders(club)
        mysql_count += 1
    for i in massive:
        i=i.lower()
        #checking = mysqlwork.check_inbase(i, club)
        checking = 0
        if i in inbase:
            checking = 1
        if os.path.exists('D:/Games/' + i) and checking:
            read = inbase[i]
            checked = check_size(read[0],read[1],dict[i])
            if checked[1] == 0:
                out_of_range.append(i)
            print '  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + str(read[0]).ljust(6) + 'MB'.ljust(5) + str(checked[0])
            f.write('  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + str(read[0]).ljust(6) + 'MB'.ljust(5) + str(checked[0])+ '\n')
            if checked[1] == 0:
                #mysqlwork.write_folder(i, dict[i], club, comp, 1,0)
                mass_to_mysql.append((i, dict[i], club, comp, 1,0))
            else:
                #mysqlwork.write_folder(i, dict[i], club, comp, 1,1)
                mass_to_mysql.append((i, dict[i], club, comp, 1,1))
        if checking == 0 and os.path.exists('D:/Games/' + i):
            print '  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + 'No data for this folder!'
            f.write('  ' + i.ljust(30) + '\t' + dict[i] + ' MB' + '\n')
            #mysqlwork.write_folder(i, dict[i], club, comp, 0,1)
            mass_to_mysql.append((i, dict[i], club, comp, 0,1))
        if os.path.exists('D:/Games/' + i) == False:
            print '  ' + i.ljust(30)+ '\t' + 'No exist!'
            f.write('  ' + i.ljust(30)+ '\t' + 'No exist!'+ '\n')
    print '\n'
    f.write ('\n')
    f.close()
    if mass_to_mysql <> []:
        mysqlwork.write_mass(mass_to_mysql)
        mysql_count += 1

def check():
    global mysql_count
    old = time.time()
    compare = []
    nocompare = []
    nohave = []
    i=0
    expected_list=mysqlwork.read_needsfolder(club)
    mysql_count += 1
    realy_list = os.listdir('D:/Games')
    for elem in realy_list:
        realy_list[i]=elem.lower()
        i=i+1
    for words in realy_list:
        print 'Calculate size for ' + 'D:/Games/' + words
        dict[words] = get_size('D:/Games/' + words)
        if words in expected_list != 1:
            compare.append(words)
        else:
            nocompare.append(words)
    mysqlwork.drop_comp(club, comp)
    mysql_count += 1
    for words in expected_list:
        if words not in realy_list != 1:
            nohave.append(words)
    if len(nohave) != 0:
        formatprint ('Folders that does not exist: ', nohave)
    formatprint('Unwanted folders: ', nocompare)
    formatprint('Converges folder: ', compare)
    if len(sys.argv) == 2 and sys.argv[1]  == 'del' and len(nocompare) != 0:
        delfolder(nocompare)
        formatprint('Deleted files and folders: ', nocompare)
    formatprint('Time for operation: ' + str(time.time() - old))
    if len(sys.argv) == 2 and sys.argv[1]  == 'restore':
        if len(nocompare) !=0:
            delfolder(nocompare)
            formatprint('Deleted files and folders: ', nocompare)
        else:
            write_log('No folders needs to delete!')
        if len(nohave) !=0:
            restore_game.add(nohave)
        else:
            write_log('No folders needs to downloading!')
        if len(out_of_range) !=0:
            restore_game.restore(out_of_range)
        else:
            write_log('No folders need to restore!')


def main():
    if len(sys.argv) > 2:
        print 'Wrong numbers of parameters!'
        sys.exit(1)

    filename = 'D:\log\Dlog.txt'
    f = open (filename, 'w')
    time = datetime.datetime.now()
    f.write('Time: ' + str(time) + '\n\n')
    f.close()
    formatprint ('Check from database!')
    if len(sys.argv) == 2 and sys.argv[1]  == 'del':
        formatprint('!Running with deleting unwanted folders!')
    if len(sys.argv) == 2 and sys.argv[1]  == 'restore':
        formatprint('!Running with restoring all data!')
    check()

if __name__ == '__main__':
    dict = {}
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    main()
    write_log('Total count of MySQL operation: '+ str(mysql_count))
    sys.exit()


