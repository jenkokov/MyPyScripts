import os
import sys
import socket
import time
import mysqlavp
import logging


general_log = 'C:\\dslogon\\general.log'
if not os.path.exists(general_log):
    os.makedirs('C:\\dslogon')
    f = open(general_log, 'a')
    f.close()
logging.basicConfig(filename=general_log, level=logging.INFO,
                    format='%(asctime)s: [avp.py] [%(levelname)s] %(message)s')


def get_time(param='w'):
    """
    If param = w: return YYYY-mm-dd / HH:MM
    Else: param YYYYmmddHHMMSS
    """
    t = time.localtime()
    if param == 'w':
        return '{0}-{1}-{2} / {3}:{4}'.format(t[0], str(t[1]).zfill(2), str(t[2]).zfill(2), str(t[3]).zfill(2), str(t[4]).zfill(2),)
    else:
        return str(t[0]) + str(t[1]).zfill(2) + str(t[2]).zfill(2) + str(t[3]).zfill(2) + str(t[4]).zfill(2) + str(t[5]).zfill(2)


def main(argv):
    status = 1
    if os.path.exists('D:\\'):
        f = open('D:\\log\log.txt', 'a')
        if argv == 'start':
            status = 0
            f.write('{0} Starting AVP...\n'.format(get_time('w').ljust(25)))
            logging.info('Starting AVP')
        if argv == 'end':
            status = 1
            f.write('{0} Finishing AVP!\n'.format(get_time('w').ljust(25)))
            logging.info('Finishing AVP')
        f.close()

    needContinue = True
    count = 0
    while needContinue:
        try:
            if mysqlavp.check_inbase(club, comp) == 0:
                mysqlavp.insert(club, comp, argv, get_time(), status)
            else:
                mysqlavp.update(club, comp, argv, get_time(), status)
            needContinue = False
        except:
            count += 1
            if count < 6:
                print 'Error to connect to DB! Try {0} of 5. Retry after 20 second... '.format(count)
                time.sleep(15)
                needContinue = True
            else:
                needContinue = False
                logging.error('Error to connect to database.')


if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    if len(sys.argv) != 2:
        print 'Wrong number of param!'
        sys.exit()
    else:
        main(sys.argv[1])