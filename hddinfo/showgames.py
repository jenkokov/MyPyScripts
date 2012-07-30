import sys
import mysqlwork
import datetime

class Folder ():
    def __init__(self, size, accuracy, status,InRange):
        self.size = size
        self.accuracy = accuracy
        self.status = status
        self.InRange = InRange

    def __repr__(self):
        f = [self.size, self.accuracy, self.status, self.InRange]
        return f

def main(club, comp):
    array = mysqlwork.read_all_folders(club, comp)
    for i in array:
        d[i[0]]=Folder(i[1],i[2],i[3],i[4])
    needs_folder = mysqlwork.read_needsfolder(club)
    print '\n+'.ljust(75,'-')+'+\n' +'|'+'Name'.center(25)+'|'+'Size'.center(11)+'|'+'Ideal'.center(11)+'|Difference'.ljust(12)+'|'+'Status'.center(11)+'|'+'\n'+'+'.ljust(74,'-')+'+'
    for name in needs_folder:
        if name not in d:
            ideal_size = mysqlwork.read(name, club)
            print '|'+name[:25].ljust(25)+'| no data'.ljust(12)+'| '+str(ideal_size[0]).ljust(10) +'| '+ str(ideal_size[0]).ljust(10)+'| NO EXISTS!|'
    for name in sorted(d):
        status='Need'
        if d[name].status == 0:
            status = 'NO NEED!'
            print '|'+name[:25].ljust(25)+'| '+ str(d[name].size).ljust(10)+'| NO DATA!'.ljust(12) +'| '+ str(d[name].size).ljust(10)+'| '+status.ljust(10)+'|'
        else:
            ideal_size = mysqlwork.read(name, club)
            print '|'+name[:25].ljust(25)+'| '+ str(d[name].size).ljust(10)+'| '+ str(ideal_size[0]).ljust(10) +'| '+ str(abs(d[name].size-ideal_size[0])).ljust(10)+'| '+status.ljust(10)+'|'
    print '+'.ljust(74,'-')+ '+\n'

def info_club(club):
    all_comp = mysqlwork.read_all_comp(club)
    needs_folder = mysqlwork.read_needsfolder(club)
    f = open ('D:/log/Log_for_Club{0}.txt'.format(club), 'w')
    time = datetime.datetime.now()
    f.write('Time: ' + str(time) + '\n\n')
    all_comp.sort()
    for machine in all_comp:
        d={}
        out_of_range=[]
        not_exist=[]
        array = mysqlwork.read_all_folders(club, machine)
        for i in array:
            d[i[0]]=Folder(i[1],i[2],i[3],i[4])
        for name in d:
            if d[name].InRange == 0:
                out_of_range.append(name)
        for name in needs_folder:
            if name not in d:
                not_exist.append(name)
        if len(out_of_range)!=0 or len(not_exist)!=0:
            print '\nErrors on {0} comp:'.format(machine)
            f.write('\nErrors on {0} comp:\n'.format(machine))
            j=1
            out_of_range.sort()
            not_exist.sort()
            for i in not_exist:
                print '\t{1}. {0} not exist!'.format(i.upper(), j).ljust(35,'.')+' <NONE>'
                f.write('\t{1}. {0} not exist!\n'.format(i.upper(), j))
                j=j+1
            for i in out_of_range:
                ideal_size = mysqlwork.read(i, club)
                delta_size = abs(d[i].size-ideal_size[0])
                print '\t{1}. {0} not in range for '.format(i.upper(),j).ljust(35,'.')+ ' {0} MB'.format(delta_size)
                f.write('\t{1}. {0} not in range for '.format(i.upper(),j).ljust(35,'.')+ ' {0} MB\n'.format(delta_size))
                j=j+1
    f.close()

if __name__ == '__main__':
    d={}
    if len(sys.argv)==3:
        main(sys.argv[1], sys.argv[2])
    if len(sys.argv)==2:
        info_club(sys.argv[1])
    sys.exit()