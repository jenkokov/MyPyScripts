import socket
import mysqlgame
import sys
from win32com.client import Dispatch
import ConfigParser
import os


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
        if Version == '':
            Version = '1.0 (by Default)'
        mysqlgame.create_game(game,addslashes(game_exe),method,Version)
        print 'Successful! Import version {0} for {1}.'.format(Version,game)

    if method == '2':
        section = raw_input('Section on INI file: ')
        value = raw_input('Value on section {0}: '.format(section))
        Version=method2(game_exe,section,value)
        if Version == '':
            Version = '1.0 (by Default)'
        mysqlgame.create_game(game,addslashes(game_exe),method,Version)
        print 'Successful! Import version {0} for {1}.'.format(Version,game)

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    club = ip.split('.')[2]
    comp = ip.split('.')[3]
    config = ConfigParser.RawConfigParser()
    while True:
        game = raw_input('Name of new game: ')
        game_exe = raw_input('Path to game file: ')
        if os.path.exists(game_exe) == False:
            print '{0} not exist!'.format(game_exe)
            continue
        method=raw_input('Method (1 - Version of file, 2 - From *.INI file): ')
        main(game,method,game_exe)

