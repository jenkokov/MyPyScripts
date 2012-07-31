import socket
import mysqlgame
import sys
from win32com.client import Dispatch
import ConfigParser

def addslashes(s):
    dict = {"\0":"\\\0", "\\":"\\\\"}
    return ''.join(dict.get(x,x) for x in s)

def method1(exe):
    ver_parser = Dispatch('Scripting.FileSystemObject')
    Version = ver_parser.GetFileVersion(exe)
    return Version

def method2(exe, section,value):
    config.read(exe)
    Version=config.get(section,value)
    return Version

def main(game, method ,game_exe):
    """
    Method 1:
    Use add_game.py [NAME OF GAME] [METHOD] [PATH TO GAME EXE]
    Take version from file [PATH TO GAME EXE].

    Method 2:
    Use add_game.py [NAME OF GAME] [METHOD] [PATH TO GAME EXE] [SECTION NAME] [PARAM NAME]
    Take version from *.ini file [PATH TO GAME EXE]. Need to know [SECTION NAME] and [PARAM NAME] where write version.
    """
    if method == '1':
        Version = method1(game_exe)
        mysqlgame.create_game(game,addslashes(game_exe),method,Version)
        print 'Successful! Import version {0} for {1}.'.format(Version,game)

    if method == '2':
        if len(sys.argv) != 6:
            print 'For this method use add_game.py [NAME OF GAME] [METHOD] [PATH TO GAME EXE] [SECTION NAME] [PARAM NAME]'
        else:
            Version=method2(game_exe,sys.argv[4],sys.argv[5])
            mysqlgame.create_game(game,addslashes(game_exe),method,Version)
            print 'Successful! Import version {0} for {1}.'.format(Version,game)

if __name__ == '__main__':
    dict = {}
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    config = ConfigParser.RawConfigParser()
    if len(sys.argv)>= 4 and len(sys.argv)<= 6:
        main(sys.argv[1], sys.argv[2],sys.argv[3])
    else:
        print 'Wrong numbers of parameters! Use add_game.py [NAME OF GAME] [METHOD] [PATH TO GAME EXE]'
