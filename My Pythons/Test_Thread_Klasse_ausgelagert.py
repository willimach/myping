import time
import threading
import sys

from Test_Thread_Library import MyClass


t = MyClass()
t.start()

try:
    while 1:
        print('Hannes rockt!')
        time.sleep(0.5)
except(KeyboardInterrupt):
    t.stop_thread()
    sys.exit()

