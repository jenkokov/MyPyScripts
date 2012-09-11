import sys
import socket
import time
import mysqlavp

def get_time():
    t = time.localtime()
    return '{0}-{1}-{2} / {3}:{4}'.format(t[0],str(t[1]).zfill(2),str(t[2]).zfill(2),str(t[3]).zfill(2),str(t[4]).zfill(2),)

def main(argv):
    f=open('D:\\log\log.txt','a')
    if argv == 'start':
        status = 0
        f.write('{0} Starting AVP...\n'.format(get_time().ljust(25)))
    if argv == 'end':
        status = 1
        f.write('{0} Finishing AVP!\n'.format(get_time().ljust(25)))
    f.close()
    if mysqlavp.check_inbase(club,comp) == 0:
        mysqlavp.insert(club,comp,argv,get_time(),status)
    else:
        mysqlavp.update(club,comp,argv,get_time(),status)

if __name__=='__main__':
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    if len(sys.argv) !=2:
        print 'Wrong number of param!'
        sys.exit()
    else:
        main(sys.argv[1])