import os
import sys
import shutil

def main():
    need_folders = ['Games', 'log','info','work']
    work_folder=u'D:/'
    all_folders=os.listdir(work_folder)
    for name in all_folders:
        if name not in need_folders:
            if os.path.isdir(work_folder+ name) == 1:
                try:
                    shutil.rmtree(work_folder+ name, 1)
                except:
                    print 'Error deleting {0}'.format(work_folder+name)
            else:
                try:
                    os.remove(work_folder+ name)
                except:
                    print 'Error deleting {0}'.format(work_folder+name)
if __name__ == '__main__':
    if len(sys.argv)<2:
        print 'Need are some one any parameter for cleaning!'
        sys.exit()
    main()
    sys.exit()