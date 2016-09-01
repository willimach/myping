import time
import os, platform,sys,threading
from datetime import datetime
from mylibrary import *

global t
t=threading.Timer(1,mycompressor)
t.start()
while 1:
    try:
        pstr=myping()
        if all(pstr):
            log=open('pinglog.txt','a')
            log.write(mytime()+'\t myping OK!\n')
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
