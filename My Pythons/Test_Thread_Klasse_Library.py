import time

def myfunc(flag):

    while flag:
        print('Hannes rockt auch in der Funktion!')
        time.sleep(0.5)

from threading import Thread

class MyClass(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.__stop = False

    def stop_thread(self):
        self.__stop = True

    def run(self):
        while not self.__stop:
            print('Hannes rockt auch in der Funktion!')
            time.sleep(0.5)
        
