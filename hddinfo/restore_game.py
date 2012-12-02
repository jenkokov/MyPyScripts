__author__ = 'Jenko'
from comparegames import write_log

def add(array):
    write_log('\nAdding {0} games...\n'.format(len(array)))
    for i in array:
        write_log('Downloading {0}...'.format(i))

def restore (array):
    write_log('\nRestoring {0} games...\n'.format(len(array)))
    for i in array:
        write_log('Repair {0}...'.format(i))

if __name__ == '__main__':
    print 'System file! Can\'t run!'