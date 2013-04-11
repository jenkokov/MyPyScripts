import os
import sys
import shutil
import time


def main():
    need_folders = ['Games', 'log']
    work_folder = u'D:/'
    all_folders = os.listdir(work_folder)
    for name in all_folders:
        if name not in need_folders:
            if os.path.isdir(work_folder + name) == 1:
                try:
                    shutil.rmtree(work_folder + name, True)
                except:
                    print 'Error deleting {0}'.format(work_folder + name)
            else:
                try:
                    os.remove(work_folder + name)
                except:
                    print 'Error deleting {0}'.format(work_folder + name)


def clear_log():
    gen_dic = 'C:\\dslogon\\'
    dic = os.listdir(gen_dic)
    r_time = time.time()
    for i in dic:
        if r_time - os.path.getmtime(gen_dic + i) > 259200:
            try:
                print 'Removing {0}.'.format(gen_dic + i)
                os.remove(gen_dic + i)
            except:
                pass


def steam_clear():
    need_folders = ['sourcemods', 'common', 'temp']
    work_folder = u'D:\\Games\\Steam\\steamapps\\'
    all_folders = os.listdir(work_folder)
    for name in all_folders:
        if name not in need_folders and os.path.isdir(work_folder + name) == 1:
            try:
                shutil.rmtree(work_folder + name, True)
            except:
                print 'Error deleting {0}'.format(work_folder + name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Need are some one any parameter for cleaning!'
        sys.exit()
    main()
    steam_clear()
    clear_log()
    sys.exit()