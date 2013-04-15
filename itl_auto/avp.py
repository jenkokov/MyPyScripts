# -*- coding: utf-8 -*-
from subprocess import call
import os
import shutil
import glob
import socket
import ConfigParser
from multiprocessing import Process

config = ConfigParser.RawConfigParser()
ip = socket.gethostbyname(socket.gethostname())
club = ip.split('.')[2]
comp = ip.split('.')[3]
server = '.'.join(ip.split('.')[:-1]) + '.252'


def run(path):
    try:
        call(path, shell=True)
    except:
        os.system(path)


def n_run(path):
    p = Process(target=run, args=(path,))
    p.start()
    p.join()
    return


def delete(name):
    if os.path.exists(name):
        if os.path.isdir(name) == 1:
            try:
                print 'Deleting ' + name
                shutil.rmtree(name, True)
            except:
                print 'Error deleting {0}'.format(name)
        else:
            try:
                print 'Deleting ' + name
                os.remove(name)
            except:
                print 'Error deleting {0}'.format(name)
    else:
        print  name + ' not exist.'


def clean():
    f = open(r'\\{0}\icons\clean_block.ini'.format(server))
    for path in f:
        name = path[:-1]
        if name[0] == '#':
            continue
        if name[-1] == '*':
            files = glob.glob(name)
            for f in files:
                delete(f)
        else:
            delete(name)


def run_module():
    n_run(r'\\{0}\standartgames\Settings\DeadSpace2_pub_files.exe'.format(server))
    run(r'\\{0}\standartgames\Settings\CrimeCraft_setting.exe'.format(server))


def main():
    #clean()
    run_module()

if __name__ == '__main__':
    main()