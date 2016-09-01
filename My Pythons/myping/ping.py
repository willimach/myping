#!python3
import threading, time
from queue import Queue
from ping_lib import *
hosts=['www.google.com','www.facebook.com','www.wikipedia.com','www.yahoo.com','www.twitter.com']


# lock to serialize console output
lock = threading.Lock()

def do_work(item):
    tname=int(threading.current_thread().name[7:])-1
    x=ping(hosts[tname])
    my_t=mytime()
    # Make sure the whole print completes or threads can mix up output in one line.
    with lock:
        log=open('pinglog.txt','a')
        if x: log.write(my_t[0]+'\t'+str(my_t[1])+ '\tping OK!'+'\t'+str(tname)+'\n')
        else: log.write(my_t[0]+'\t'+str(my_t[1])+ '\t'+ str(x)+'\t'+str(tname)+'\n')
        os.fsync(log)
        log.close()
        #print(threading.current_thread().name,tname, my_t, x,hosts[tname])

# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()


maintenanceFlag=True
def maintenance():
    while maintenanceFlag:
        if datetime.now().minute==0:
            os.system("python3 speedtest_w.py --simple")
            time.sleep(5)
            mycompressor()
            time.sleep(5)
            plotter()
            time.sleep(5)
            myftp()
try:        
    # Create the queue and thread pool.
    q = Queue()
    for i in range(len(hosts)):
         t = threading.Thread(target=worker)
         t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
         t.start()
         
    t2=threading.Thread(target=maintenance)
    t2.daemon=True
    t2.start()

    # stuff work items on the queue (in this case, just a number).
    start = time.perf_counter()

    #for item in range(10):
    #    q.put()
    while 1:
        time.sleep(1)
        q.put(12)
    q.join()       # block until all tasks are done

except(KeyboardInterrupt):
    maintenanceFlag=False
    print('Willis KeyboardInterrupt')
