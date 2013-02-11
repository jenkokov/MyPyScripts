logfile_name = 'D:\log\Dlog.txt'


def write_log(string):
    f = open(logfile_name, 'a')
    print string
    f.write(string + '\n')
    f.close()


def add(array):
    """
Download all folders in "array"
    """
    write_log('\nAdding {0} games...\n'.format(len(array)))
    for i in array:
        write_log('Downloading {0}...'.format(i))


def restore(array):
    """
Delete and download all folders in "array"
    """
    write_log('\nRestoring {0} games...\n'.format(len(array)))
    for i in array:
        write_log('Repair {0}...'.format(i))

if __name__ == '__main__':
    print 'System file! Can\'t run!'