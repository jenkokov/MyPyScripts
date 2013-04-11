# -*- coding: utf-8 -*-
from subprocess import call
from subprocess import check_call as w_call
from subprocess import check_output as n_call
import os
import shutil
import glob


def delete(name):
    if os.path.exists(name):
        if os.path.isdir(name) == 1:
            try:
                shutil.rmtree(name, True)
            except:
                print 'Error deleting {0}'.format(name)
        else:
            try:
                os.remove(name)
            except:
                print 'Error deleting {0}'.format(name)
    else:
        print  name + ' not exist.'


def clean():
    f = open('clean_block.ini')
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