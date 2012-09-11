import sys
import socket
import time
import mysqlavp

def get_time():
    t = time.localtime()
    return '{0}-{1}-{2} / {3}:{4}'.format(t[0],t[1],t[2],t[3],t[4])

def main(argv):
    if mysqlavp.check_inbase(club,comp) == 0:
        mysqlavp.insert(club,comp,argv,get_time())
    else:
        mysqlavp.update(club,comp,argv,get_time())

if __name__=='__main__':
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    if len(sys.argv) !=2:
        print 'Wrong number of param!'
        sys.exit()
    else:
        main(sys.argv[1])