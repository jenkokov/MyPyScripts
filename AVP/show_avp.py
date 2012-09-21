import mysqlavp
import time
import send_mail
from datetime import datetime

def get_duration(s,e):
    #duration = get_duration(i[2].split(' / ')[1], i[3].split(' / ')[1]
    if s==None or e==None:
        return 'No data!'
    #start = s.split(' / ')[1]
    #end = e.split(' / ')[1]
    t1 = datetime.strptime(str(s),'%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime(str(e),'%Y-%m-%d %H:%M:%S')
    return str((t2 - t1))



def get_time():
    t = time.localtime()
    return '{0}-{1}-{2} / {3}:{4}'.format(t[0],str(t[1]).zfill(2),str(t[2]).zfill(2),str(t[3]).zfill(2),str(t[4]).zfill(2))

def sendmail(mail):
    print 'Sending mail to {0}...'.format(mail)
    send_mail.send_mail(mail,'AVP log from all clubs {0}'.format(get_time()),'Logs file in attachment!',log)
    print 'Successful send email!'


def main(sorting):
    clubs=['10','11','12','20']
    f=open(log,'w')
    for club in clubs:
        ss = '\nLogs for club #{0}'.format(club)
        print ss
        f.write(ss+'\n')

        ss = '+'.ljust(93,'-')+'+\n|Comp'.ljust(8)+'|Start'.ljust(26)+'|End'.ljust(26)+'|Status'.ljust(15)+'|Duration'.ljust(20)+'|\n+'+''.ljust(92,'-')+'+'
        print ss
        f.write(ss+'\n')

        d = mysqlavp.select_club(club,sorting)
        for i in d:
            #print i
            duration = get_duration(i[2], i[3])
            status='Not finished!'
            if i[5] == 1:
                status='Successful!'
            ss = '|'+str(i[1]).ljust(5)+'|'+str(i[2]).ljust(25)+'|'+str(i[3]).ljust(25)+'|'+status.ljust(14)+'|'+duration.ljust(19)+'|'
            print ss
            f.write(ss+'\n')

        ss = '+'.ljust(93,'-')+'+'
        print ss
        f.write(ss+'\n')
    f.close()


if __name__ == '__main__':
    #log='/tmp/AVP_Summary.txt'
    log = 'D:\\log\\AVP_Summary.txt'
    Sorting = raw_input('Sorting (default by start time): ')
    if Sorting == '':
        Sorting = 'start'
    mail = raw_input('E-mail for send logs (if no need empty): ')
    d = []
    main(Sorting)
    if mail != '':
        sendmail(mail)
    Sorting = 'start'
    #mail = ['jenko.kov@gmail.com','diablik@online.ua','shad.itland@gmail.com']
    #sendmail(mail)