import os
import sys
import shutil
import win32ui
import win32con



def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except:
                return False
    return total_size

def scan_games(size, folders, files, accuracy=100):
    size_check= True
    folders_check= True
    files_check= True
    total_size = 0
    miss_folders=[]
    miss_files=[]
    for name in folders:
        fsize = get_size(name)
        if fsize == False:
            miss_folders.append(name)
            folders_check= False
        else:
            total_size += fsize
    for name in files:
        try:
            total_size += os.path.getsize(name)
        except:
            miss_files.append(name)
            files_check= False
    total_size = total_size/1024/1024
    if abs(total_size-size) > accuracy:
        size_check = False

    if size_check == True:
        print 'Size check COMPLETE without errors! ({0} MB)'.format(total_size)
    else:
        print 'Size check FAILED! Out of range for {0} MB.'.format(abs(total_size-size))

    if files_check == True:
        print 'Files check COMPLETE without errors! {0} file(s) exists.'.format(len(files))
    else:
        print 'Files check FAILED! {0} file(s) not exist'.format(len(miss_files))

    if folders_check == True:
        print 'Folders check COMPLETE without errors! {0} file(s) exists.'.format(len(folders))
    else:
        print 'Folders check FAILED! {0} folder(s) not exist'.format(len(miss_folders))
    #o = win32ui.CreateFileDialog( 1, None, None,(win32con.OFN_FILEMUSTEXIST|win32con.OFN_EXPLORER|win32con.OFN_ALLOWMULTISELECT), "Text Files (*.txt)|*.txt|All Files (*.*)|*.*|")
    #o.DoModal()
    #print o.GetPathName()

def main():
    start_path = 'D:\\Games\\steam\\steamapps'
    list=[]
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            list.append(fp)
            print fp
    print len(list)

if __name__ == '__main__':
    folders=['D:\\Games\\Steam\\steamapps\\common\\aliens vs predator\\']
    files=["D:\\Games\\Steam\\steamapps\\aliens vs predator english.ncf", "D:\\Games\\Steam\\steamapps\\aliens vs predator executables.ncf",
           "D:\\Games\\Steam\\steamapps\\aliens vs predator public core.ncf","D:\\Games\\Steam\\steamapps\\aliens vs predator russian.ncf"]
    scan_games(15050,folders,files)
    #main()