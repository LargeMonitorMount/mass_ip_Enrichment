from threading import Thread
import time

def time1(a, b):
    print (a)
    time.sleep(10)
    print (time.time(), a)
    return (b)

def time2(c, d):
    print (c)
    time.sleep(10)
    print (time.time(), c)
    return d

if __name__ == '__main__':
    # target: the function name (pointer),
    # args: a tuple of the arguments that you want to send to your function
    t1 = Thread(target = time1, args=(1, 2))
    t2 = Thread(target = time2, args=(3, 4))

    # start the functions:
    a = t1.start()
    b = t2.start()
    print (a)
    print (b)