# -*- coding: utf-8 -*-
import mysqlavp
import time
import send_mail
from datetime import datetime


def get_duration(s, e):
    if not s or not e:
        return 'No data!'
    t1 = datetime.strptime(str(s), '%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime(str(e), '%Y-%m-%d %H:%M:%S')
    return str((t2 - t1))


def get_time():
    t = time.localtime()
    return '{0}-{1}-{2} / {3}:{4}'.format(t[0], str(t[1]).zfill(2), str(t[2]).zfill(2), str(t[3]).zfill(2), str(t[4]).zfill(2))


def sendmail(mail):
    print 'Передача письма на {0}...'.format(mail)
    send_mail.send_mail(mail, 'AVP лог со всех клубов за {0}'.format(get_time()), 'Файл в прикрепленных файлах', log)
    print 'Успешно передан.'


def main(sorting):
    clubs = ['10', '11', '12', '20']
    f = open(log, 'w')
    for club in clubs:
        ss = '\nLogs for club #{0}'.format(club)
        print ss
        f.write(ss + '\n')
        ss = '+'.ljust(93, '-') + '+\n|Comp'.ljust(8) + '|Start'.ljust(26) + '|End'.ljust(26) + '|Status'.ljust(15) + \
             '|Duration'.ljust(20) + '|\n+' + ''.ljust(92, '-') + '+'
        print ss
        f.write(ss + '\n')

        d = mysqlavp.select_club(club, sorting)
        for i in d:
            duration = get_duration(i[2], i[3])
            status = 'Not finished!'
            if i[5] == 1:
                status = 'Successful!'
            ss = '|' + str(i[1]).ljust(5) + '|' + str(i[2]).ljust(25) + '|' + str(i[3]).ljust(25) + \
                 '|' + status.ljust(14) + '|' + duration.ljust(19) + '|'
            print ss
            f.write(ss + '\n')

        ss = '+'.ljust(93, '-') + '+'
        print ss
        f.write(ss + '\n')
    f.close()


if __name__ == '__main__':
    log = 'AVP_Summary.txt'
    main('start')
    mail_dict = ['jenko.kov@gmail.com', 'diablik86@gmail.com', 'l.masya777@gmail.com', 'hok.life@gmail.com']
    for mail in mail_dict:
        sendmail(mail)
    #Sorting = raw_input('Sorting (default by start time): ')
    #if Sorting == '':
    #    Sorting = 'start'
    #mail = raw_input('E-mail for send logs (if no need empty): ')
    #main(Sorting)
    #if mail != '':
    #    sendmail(mail)
    #Sorting = 'start'
