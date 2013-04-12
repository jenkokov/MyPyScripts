# -*- coding: utf-8 -*-
from subprocess import call
import os
import shutil
import glob
import socket

ip = socket.gethostbyname(socket.gethostname())
club = ip.split('.')[2]
comp = ip.split('.')[3]


def run(path):
    try:
        call(path, shell=True)
    except:
        os.system(path)


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
    f = open(r'\\172.16.10.252\icons\clean_block.ini')
    for path in f:
        name = path[:-1]
        if name[-1] == '*':
            files = glob.glob(name)
            for f in files:
                delete(f)
        else:
            delete(name)


def main():
    clean()


if __name__ == '__main__':
    main()