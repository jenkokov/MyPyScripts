import win32api
import os
import datetime
import socket


def getFileVersion(filename):
    if os.path.exists(filename):
        lang, code_page = win32api.GetFileVersionInfo(filename, '\\VarFileInfo\\Translation')[0]
        strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, code_page, 'FileVersion')
        String_File_Info = win32api.GetFileVersionInfo(filename, strInfoPath)
        return 'Version: ' + String_File_Info
    else:
        return 'File not found.'


def main():
    f = open('C:\\dslogon\\versions.txt', 'w')
    f.write(str(datetime.datetime.now()) + '\n')
    f.write('IP: ' + str(socket.gethostbyname(socket.gethostname())) + '\n')
    files_to_check = ['C:\\windows\\system32\\dslogon.dll',
                      'C:\\windows\\system32\\itlogon.dll',
                      'C:\\windows\\system32\\itlsec.dll',
                      "C:\\Program Files (x86)\\ITLSoftware\\clubnetsvc.exe",
                      "C:\\Program Files (x86)\\ITLSoftware\\Shell\\dashboard.exe",
                      "C:\\Program Files (x86)\\ITLSoftware\\Notify\\AppNotify.exe"]
    for name in files_to_check:
        f.write(name.split('\\')[-1] + ' ' + str(getFileVersion(name)) + '\n')
    f.close()

if __name__ == '__main__':
    main()
