import sys
import mysqlavp
import time
import send_mail

def get_time():
    t = time.localtime()
    return '{0}-{1}-{2} / {3}:{4}'.format(t[0],str(t[1]).zfill(2),str(t[2]).zfill(2),str(t[3]).zfill(2),str(t[4]).zfill(2),)

def sendmail(email):
    print 'Sending mail to {0}...'.format(email)
    send_mail.send_mail(email,'[TEST] AVP log from all clubs {0}'.format(get_time()),'Logs file in attachment!',"D:\\log\\AVP_Summary.txt")
    print 'Successful send email!'


def main(sorting):
    clubs=['10','11','12','20']
    f=open("D:\\log\\AVP_Summary.txt",'w')
    for club in clubs:
        ss = '\nLogs for club #{0}'.format(club)
        print ss
        f.write(ss+'\n')

        ss = '+'.ljust(73,'-')+'+\n|Comp'.ljust(8)+'|Start'.ljust(26)+'|End'.ljust(26)+'|Status'.ljust(15)+'|'
        print ss
        f.write(ss+'\n')

        d = mysqlavp.select_club(club,sorting)
        for i in d:
            status='Not finished!'
            if i[5] == 1:
                status='Successful!'
            ss = '|'+str(i[1]).ljust(5)+'|'+str(i[2]).ljust(25)+'|'+str(i[3]).ljust(25)+'|'+status.ljust(14)+'|'
            print ss
            f.write(ss+'\n')

        ss = '+'.ljust(73,'-')+'+'
        print ss
        f.write(ss+'\n')
    f.close()


if __name__ == '__main__':
    Sorting = raw_input('Sorting (default by start time): ')
    if Sorting == '':
        Sorting = 'start'
    email = raw_input('E-mail for send logs (if no need empty): ')
    d = []
    main(Sorting)
    if email != '':
        sendmail(email)