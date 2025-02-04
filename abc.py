import threading
import time



def start():
    print('started')

t1 = threading.Timer(3, start)
t1.start()