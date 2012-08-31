import sys
import os
import datetime
import shutil
import time
import mysqlwork
import socket


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
            total_size += os.path.getsize(fp)
    return str(total_size/1024/1024)

def delfolder(array):
    for i in array:
        #print('D:/Games/' + i)
        if os.path.isdir('D:/Games/'+ i) == 1:
            shutil.rmtree('D:/Games/'+ i, 1)
        else:
            os.remove("D:/Games/"+ i)
        mysqlwork.del_folder(club,comp,i)

def formatprint(string, massive=[]):
    filename = 'D:\log\Dlog.txt'
    f = open(filename, 'a')
    print string
    f.write(string + '\n')
    for i in massive:
        i=i.lower()
        if os.path.exists('D:/Games/' + i) and mysqlwork.check_inbase(i, club):
            checked = check_size(mysqlwork.read(i,club)[0],mysqlwork.read(i,club)[1],dict[i])
            print '  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + str(mysqlwork.read(i,club)[0]).ljust(6) + 'MB'.ljust(5) + str(checked[0])
            f.write('  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + str(mysqlwork.read(i,club)[0]).ljust(6) + 'MB'.ljust(5) + str(checked[0])+ '\n')
            if checked[1] == 0:
                mysqlwork.write_folder(i, dict[i], club, comp, 1,0)
            else:
                mysqlwork.write_folder(i, dict[i], club, comp, 1,1)
        if mysqlwork.check_inbase(i, club)== 0 and os.path.exists('D:/Games/' + i):
            print '  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + 'No data for this folder!'
            f.write('  ' + i.ljust(30) + '\t' + dict[i] + ' MB' + '\n')
            mysqlwork.write_folder(i, dict[i], club, comp, 0)
        if os.path.exists('D:/Games/' + i) == False:
            print '  ' + i.ljust(30)+ '\t' + 'No exist!'
            f.write('  ' + i.ljust(30)+ '\t' + 'No exist!'+ '\n')
    print '\n'
    f.write ('\n')
    f.close()

def check():
    old = time.time()
    compare = []
    nocompare = []
    nohave = []
    i=0
    mysqlwork.drop_comp(club, comp)
    expected_list=mysqlwork.read_needsfolder(club)
    #print expected_list
    realy_list = os.listdir('D:/Games')
    for elem in realy_list:
        realy_list[i]=elem.lower()
        i=i+1
    #print realy_list
    for words in realy_list:
        print 'Calculate size for ' + 'D:/Games/' + words
        dict[words] = get_size('D:/Games/' + words)
        if words in expected_list != 1:
            compare.append(words)
        else:
            nocompare.append(words)
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
    check()

if __name__ == '__main__':
    dict = {}
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    main()
    sys.exit()


