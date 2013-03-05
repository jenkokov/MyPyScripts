import socket
import mysqlgame
import add_game


class Game ():
    def __init__(self, EXEpath, method, ActualVersion):
        self.EXEpath=EXEpath
        self.method=method
        self.ActualVersion=ActualVersion

    def __repr__(self):
        f = [self.EXEpath,self.method,self.ActualVersion]
        return f


def main():
    bad_games=[]
    good_games=[]
    array = mysqlgame.games_version(club)
    for i in array:
        d[i[0]]=Game(i[1],i[2],i[3])
    for name in d:
        method = d[name].method
        if method == 1:
            LocalVersion=add_game.method1(d[name].EXEpath)
            if LocalVersion == '':
                LocalVersion = '1.0 (by Default)'
        if LocalVersion != d[name].ActualVersion:
            bad_games.append(name)
            print '{0} have bad version ({1})! Need version: {2}'.format(name,LocalVersion, d[name].ActualVersion)
        else:
            good_games.append(name)
            print '{0} have good version ({1})'.format(name,LocalVersion)

if __name__ == '__main__':
    d={}
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    main()