import os
import shutil


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

steam_clear()