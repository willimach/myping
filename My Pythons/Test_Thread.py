import time, threading,sys

def myfunc():
    while flag:
        print('Hannes rockt auch in der Funktion!')
        time.sleep(0.5)

t=threading.Thread(target=myfunc)
flag=True
t.start()

try:
    while 1:
        print('Hannes rockt!')
        time.sleep(0.5)
except(KeyboardInterrupt):
    flag=False
    sys.exit()
