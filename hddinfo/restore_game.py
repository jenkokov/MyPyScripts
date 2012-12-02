__author__ = 'Jenko'

def add(array):
    print '\nAdding {0} games...\n'.format(len(array))
    for i in array:
        print 'Downloading {0}...'.format(i)

def restore (array):
    print '\nRestoring {0} games...\n'.format(len(array))
    for i in array:
        print 'Repair {0}...'.format(i)

if __name__ == '__main__':
    print 'System file! Can\'t run!'