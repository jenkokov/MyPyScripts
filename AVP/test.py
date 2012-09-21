import time
import datetime
def get_time():
    t = time.localtime()
    return str(t[0])+str(t[1]).zfill(2)+str(t[2]).zfill(2)+str(t[3]).zfill(2)+str(t[4]).zfill(2)+str(t[5]).zfill(2)

print get_time()