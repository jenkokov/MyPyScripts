import mysqlavp
import time
import sys


def get_datetime(val='datetime'):
    t = time.localtime()
    if val == 'datetime':
        return '{0}-{1}-{2} / {3}:{4}:{5}'.format(t[0], str(t[1]).zfill(2), str(t[2]).zfill(2), str(t[3]).zfill(2),
                                                  str(t[4]).zfill(2), str(t[5]).zfill(2))
    if val == 'date':
        return '{0}-{1}-{2}'.format(t[0], str(t[1]).zfill(2), str(t[2]).zfill(2))
    if val == 'time':
        return '{0}:{1}:{2}'.format(str(t[3]).zfill(2), str(t[4]).zfill(2), str(t[5]).zfill(2))


def main():
    sdate = raw_input("Input start date (YYYY-MM-DD): ")
    fdate = raw_input('Input end date (if one day empty): ')
    if sdate == '':
        sdate = get_datetime('date')
    if fdate == '':
        fdate = sdate
        print 'Logs for {0}'.format(sdate)
        f = open("D:\\log\\uTorrent_Summary[{0}].log".format(sdate), 'w')
    else:
        print 'Logs from {0} to {1}\n'.format(sdate, fdate)
        f = open("D:\\log\\uTorrent_Summary[{0}-{1}].log".format(sdate, fdate), 'w')
    clubs = ['10', '11', '12', '20']
    for club in clubs:
        d = mysqlavp.select_torrent(club, sdate, fdate)
        ncomps = mysqlavp.check_comp(club, sdate, fdate)
        if d == ():
            ss = 'No info for club #{0}'.format(club)
            print ss
            f.write(ss + '\n')
        else:
            ss = 'Log uTorrent for club #{0}\n'.format(club) + '+'.ljust(67, '-') + '+\n' + \
                 '|Comp ' + '|Date'.ljust(13) + '|Time'.ljust(11) + '|Torrent'.ljust(21) + '|Status'.ljust(16) + \
                 '|\n' + '+'.ljust(67, '-') + '+'
            print ss
            f.write(ss + '\n')
            for i in d:
                ss = '|' + str(i[0]).ljust(5) + '|' + str(i[1]).ljust(12) + '|' + str(i[2]).ljust(10) + '|' + \
                     str(i[3]).ljust(20) + '|' + str(i[4]).ljust(15) + '|'
                print ss
                f.write(ss + '\n')
            ss = '+'.ljust(67, '-') + '+\n' + 'Comp in  club #{0} that\'s not in base:'.format(club)
            print ss
            f.write(ss + '\n')
            string = ''
            for i in ncomps:
                string = string + str(i) + ', '
            ss = string[:-2] + '.\n'
            print ss
            f.write(ss + '\n')

    f.close()
    sys.exit()

if __name__ == '__main__':
    main()
