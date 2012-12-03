import sys
import mysqlwork
import datetime

def write_log(string):
    f = open('D:\\log\\ideals.log', 'a')
    print string
    f.write(string+'\n')
    f.close()

class Folder ():
    def __init__(self, in10, in11, in12, in20):
        self.in10 = in10
        self.in11 = in11
        self.in12 = in12
        self.in20 = in20

    def __repr__(self):
        f = [self.in10, self.in11, self.in12,self.in20]
        return str(f)

def main():
    f = open('D:\\log\\ideal.log','w')
    f.close()
    all_folders = []
    d = {}
    all_data = mysqlwork.get_ideals()
    for i in all_data:
        if i[1] not in all_folders:
            all_folders.append(i[1])
    write_log('+'.ljust(21,'-')+'+--------+--------+--------+--------+\n'+\
          '|Name'.ljust(21)+'|InClub10|InClub11|InClub12|InClub20|\n'+\
          '+'.ljust(21,'-')+'+--------+--------+--------+--------+')
    for name in sorted(all_folders):
        in10 = '---'
        in11 = '---'
        in12 = '---'
        in20 = '---'
        for i in all_data:
            if i[1] == name:
                if i[0] == 10:
                    in10 = i[2]
                if i[0] == 11:
                    in11 = i[2]
                if i[0] == 12:
                    in12 = i[2]
                if i[0] == 20:
                    in20 = i[2]
        d[name]=Folder(in10, in11, in12, in20)
        write_log('|'+name.ljust(20) +'|'+ str(d[name].in10).ljust(8)+'|'+ str(d[name].in11).ljust(8)+'|'+ str(d[name].in12).ljust(8)+'|'+ \
              str(d[name].in20).ljust(8)+'|')
    write_log('+'.ljust(21,'-')+'+--------+--------+--------+--------+')
    return

if __name__ == '__main__':
    main()
