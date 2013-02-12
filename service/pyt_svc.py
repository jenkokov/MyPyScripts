import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time

global _need_stop_
_need_stop_ = False


class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "tor_check"
    _svc_display_name_ = "Torrent Check"
    _svc_description_ = "Service for check torrent tasks"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        global _need_stop_
        _need_stop_ = True
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        i = 0
        while not _need_stop_:
            time.sleep(5)
            f = open('D:\\4.txt', 'a')
            f.write(str(i) + '\n')
            i += i
            f.close()
        pass


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)