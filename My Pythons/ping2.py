import time
import os, platform
import sys
from datetime import datetime

def ping():

    """
    Returns True if host responds to a ping request
    """
    host=['www.google.com','www.facebook.com','www.wikipedia.com','www.yahoo.com','www.twitter.com']
    
    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

    # Ping
    answer=[]
    for i in range(0,len(host)):
        answer.append(os.system("ping " + ping_str + " " + host[i]) == 0)
        time.sleep(0.9)
    return(answer)


def mytime():
	mytime=datetime.now()	
	date = "%04d.%02d.%02d_%02d:%02d:%02d" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second)
	return(date)

while 1:
    try:
        pstr=ping()
        if all(pstr):
            log=open('pinglog.txt','a')
            log.write(mytime()+'\t ping OK!\n')
            os.fsync(log)
            log.close()
        else:
            log=open('pinglog.txt','a')
            log.write(mytime()+ '\t'+str(pstr)+'\n')
            os.fsync(log)
            log.close()
        time.sleep(1)
    except(KeyboardInterrupt):
        print('Willis KeyboardInterupt')
        raise SystemExit
