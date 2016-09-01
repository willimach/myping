#!python3
import threading, time,os
from queue import Queue
from ping_lib import *
from datetime import datetime
import configparser

config=configparser.ConfigParser()
config.read('ping_config.txt')
hosts=config['ping']['hosts']
#split string and strip whitespaces
hosts=list(map(str.strip,hosts.split(',')))


# lock to serialize console output
lock = threading.Lock()

def do_work(item):
    tname=int(threading.current_thread().name[7:])-1
    x=ping(hosts[tname])
    my_t=mytime()
    # Make sure the whole print completes or threads can mix up output in one line.
    with lock:
        log=open('pinglog.txt','a')
        if x: log.write(my_t[0]+ '\tping OK!'+'\t'+str(tname)+'\n')
        else: log.write(my_t[0]+ '\t'+ str(x)+'\t'+str(tname)+'\n')
        os.fsync(log)
        log.close()
        #print(threading.current_thread().name,tname, my_t, x,hosts[tname])

# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()
        
    
# Create the queue and thread pool.
q = Queue()
for i in range(len(hosts)): #just 1 thread
    t = threading.Thread(target=worker)
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()
    
# stuff work items on the queue (in this case, just a number).
while 1:
    if q.qsize() < 10: #just 10 items in queue
        q.put(12) #12 is random item
        time.sleep(1)
    if datetime.now().minute==0 and datetime.now().second<2:
        #empty queue, so compressor uses pinglog.txt exclusively
        while q.qsize()!=0: 
            time.sleep(0.01)
        mycompressor()
        plotter()
        myftp()
            
q.join()       # block until all tasks are done
