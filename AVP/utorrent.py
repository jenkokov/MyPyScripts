import sys
import time
import socket
import mysqlavp

def get_time():
    t = time.localtime()
    return '{0}-{1}-{2} / {3}:{4}'.format(t[0],str(t[1]).zfill(2),str(t[2]).zfill(2),str(t[3]).zfill(2),str(t[4]).zfill(2),)

def main():
    f=open('D:\\log\\torrent.log','a')
    torrent = sys.argv[1]
    status = status_dict[sys.argv[2]]
    if sys.argv[2] == '1':
        ff = open ('C:\\dslogon\\errors.log','a')
        ff.write('{0} [uTorrent] Error of torrent {1}!\n'.format(get_time().ljust(25),torrent))
        ff.close()
    ss = '{0} Torrent: {1} Status: {2}\n'.format(get_time().ljust(25), torrent.ljust(15),status)
    f.write(ss)
    f.close()

    needContinue = True
    count=0
    while needContinue:
        try:
            if mysqlavp.check_torrent(club,comp,torrent) == 0:
                mysqlavp.insert_torrent(club,comp,torrent,get_time(),status)
            else:
                mysqlavp.update_torrent(club,comp,torrent,get_time(),status)
            needContinue = False
        except:
            count=count+1
            if count <6:
                print 'Error to connect to DB! Try {0} of 5. Retry after 20 second... '.format(count)
                time.sleep(15)
                needContinue = True
            else:
                needContinue = False
                f=open('C:\\logs\\errors.txt','a')
                f.write('{0} [uTorrent] Error connect to DB for writing uTorrent info.\n'.format(get_time().ljust(25)))
                f.close()

    sys.exit()


if __name__=='__main__':
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    status_dict={'1':'Error!', '2':'Checking', '3': 'Pause','4':'SuperSeed','5':'Seeding',
       '6':'Downloading','7':'SuperSeed[F]','8':'Seeding[F]','9':'Downloading[F]','10':'Wait seeding',
       '11':'Complete','12':'In queue','13':'Stopped'}
    main()