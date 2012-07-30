import sys
import os
import datetime
import shutil
import time
import ConfigParser
import mysqlwork


def check_size(f_size, accuracy, r_size):
    if abs(int(f_size)-int(r_size)) > int(accuracy):
        return 'Out of range to: ' + str(abs(int(f_size)-int(r_size))-int(accuracy)) + ' MB'
    else:
        return 'Normal size!'

def get_size(start_path = '.'):
    #old = time.time()
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
        #    print 'Time: ' + str(time.time() - old)
    return str(total_size/1024/1024)

def delfolder(array):
    for i in array:
        #print('D:/Games/' + i)
        if os.path.isdir('D:/Games/'+ i) == 1:
            shutil.rmtree('D:/Games/'+ i, 1)
        else:
            os.remove("D:/Games/"+ i)
    formatprint('Deleted files and folders: ', array)

def formatprint(string, massive=[]):
    filename = 'D:\log\Dlog.txt'
    f = open(filename, 'a')
    print string
    f.write(string + '\n')
    for i in massive:
        i=i.lower()
        if os.path.exists('D:/Games/' + i) and config.has_section(i):
            print '  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + config.get(i,'size').ljust(6) + 'MB'.ljust(5) + check_size(config.get(i,'size'),config.get(i,'range'),dict[i])
            f.write('  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + config.get(i,'size').ljust(6) + 'MB'.ljust(5) + check_size(config.get(i,'size'),config.get(i,'range'),dict[i])+ '\n')

        if config.has_section(i)!=1 and os.path.exists('D:/Games/' + i):
            print '  ' + i.ljust(30) + '\t' + dict[i].ljust(6) + 'MB'.ljust(10) + 'No data for this folder!'
            f.write('  ' + i.ljust(30) + '\t' + dict[i] + ' MB' + '\n')

        if config.has_section(i) and os.path.exists('D:/Games/' + i) !=1:
            print '  ' + i.ljust(30)+ '\t' + 'No exist!'
            f.write('  ' + i.ljust(30)+ '\t' + 'No exist!'+ '\n')
    print '\n'
    f.write ('\n')
    f.close()

def check(filename):
    old = time.time()
    compare = []
    nocompare = []
    nohave = []
    i=0
    config.read(filename)
    expected_list = ConfigParser.RawConfigParser.sections(config)
    #print expected_list
    expected_list = os.listdir('D:/Games')
    for elem in expected_list:
        expected_list[i]=elem.lower()
        i=i+1
    #print expected_list
    for words in expected_list:
        dict[words] = get_size(u'D:/Games/' + words)
        if words in expected_list != 1:
            compare.append(words)
        else:
            nocompare.append(words)
    for words in expected_list:
        if words not in expected_list != 1:
            nohave.append(words)
    if len(nohave) != 0:
        formatprint ('Folders that does not exist: ', nohave)
#    if len(nocompare) == 0:
 #       formatprint('All needs folders exists!')
  #  else:
    formatprint('Unwanted folders: ', nocompare)
    formatprint('Converges folder: ', compare)
    #       for words in expected_list:
    #       print words
    #   print dict
    if len (sys.argv) == 3 and sys.argv[2]  == 'del' and len(nocompare) != 0:
        delfolder(nocompare)
    formatprint('Time for operation: ' + str(time.time() - old))

def main():
    if len(sys.argv) != 2 and len (sys.argv) != 3:
        print 'Wrong numbers of parameters!'
        sys.exit(1)

    filename = 'D:\log\Dlog.txt'
    f = open (filename, 'w')
    time = datetime.datetime.now()
    f.write('Time: ' + str(time) + '\n\n')
    f.close()
    formatprint ('Files for compare: ' + str(sys.argv[1]))
    if len (sys.argv) == 3 and sys.argv[2]  == 'del':
        formatprint('!Running with deleting unwanted folders!')
    check(sys.argv[1])

if __name__ == '__main__':
    dict = {}
    config = ConfigParser.RawConfigParser()
    main()


