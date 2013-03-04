from mysqlhard import *
import operator


def parse_free_space(diskD):
    if diskD:
        d = diskD.split(' ')
        return int(d[4][1:])
    else:
        return 'No info.'


def main():
    d = get_free_space()
    f = open('D:\\log\\Free_space.txt', 'w')
    string = '+----+-----+-------------+---------------------+\n|Club|Comp |Free space   |Time                 |\n' \
             '+----+-----+-------------+---------------------+'
    print string
    f.write(string + '\n')
    for club, comp, diskD, time in d:
        string = '|{0:3d} | {1:3d} | {2:9} MB| {3} |'.format(club, comp, str(parse_free_space(diskD)), time)
        print string
        f.write(string + '\n')
    string = '+----+-----+-------------+---------------------+'
    print string
    f.write(string)
    f.close()


def by_free_space():
    d = get_free_space()
    mass = {10: {}, 11: {}, 12: {}, 20: {}}
    f = open('D:\\log\\Free_space.txt', 'w')
    for club, comp, diskD, time in d:
        if club in mass:
            mass[club][comp] = parse_free_space(diskD)
    for club in sorted(mass):
        sorted_mass = sorted(mass[club].iteritems(), key=operator.itemgetter(1))
        string = 'Info for club #{0}\n+----+-------------+'.format(club)
        print string
        f.write(string + '\n')
        for comp in sorted_mass:
            string = '|{0:3} | {1:9} MB|'.format(comp[0], str(comp[1]))
            print string
            f.write(string + '\n')
        string = '+----+-------------+\n'
        print string
        f.write(string)


if __name__ == '__main__':
    ans = raw_input('Select sort: by comp (default) or by free space (enter \'1\'):')
    if ans == '1':
        by_free_space()
    else:
        main()