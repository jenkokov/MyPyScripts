import time
def get_time():
    t = time.localtime()
    return '{0}-{1}-{2} / {3}:{4}'.format(t[0],str(t[1]).zfill(2),str(t[2]).zfill(2),str(t[3]).zfill(2),str(t[4]).zfill(2))

f=open('C:\\dslogon\\errors.log','a')
f.write('{0} Error connect to DB for writing AVP info.\n'.format(get_time().ljust(25)))
f.close()