"""import os,filever

myPath="D:\\Games\\WoT"

for root, dirs, files in os.walk(myPath):
    for file in files:
        file = file.lower() # Convert .EXE to .exe so next line works
        if (file.count('.exe') or file.count('.dll')): # Check only exe or dll files
            fullPathToFile=os.path.join(root,file)
            major,minor,subminor,revision=filever.get_version_number(fullPathToFile)
            print "Filename: %s \t Version: %s.%s.%s.%s" % (file,major,minor,subminor,revision)
"""
from win32com.client import Dispatch

path='D:\Games\WoT\WorldOfTanks.exe'
ver_parser = Dispatch('Scripting.FileSystemObject')
info = ver_parser.GetFileVersion(path)
print info

if info == 'No Version Information Available':
    info = None