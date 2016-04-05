#!/usr/bin/python

import threading
import time

global quad_state
quad_state = "disarmed"


# Define a function for the thread
def print_time( threadName, delay):
    global quad_state
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        me = threading.current_thread()
        print ("%s: %s  -- Quad State: %s\n" % ( threadName, time.ctime(time.time()), quad_state))
        #print(me.name)

#quad_state = "disarmed"
def quad_controller():
    global quad_state
    quad_state = "armed"
    count = 0
    while count < 5:
        time.sleep(1.5)
        count += 1
        print("%s: %s  -- Quad State: %s\n" %(threading.current_thread().name, time.ctime(), quad_state))
    quad_state = "disarmed"

# Create two threads as follows
##try:
##   
##except:
##    
##   print("Error: unable to start thread")

threading.Thread( target=print_time, args=("Thread-1", 2, ), name='First Thread' ).start()
threading.Thread( target=print_time, args=("Thread-2", 4, ), name='Second Thread' ).start()
threading.Thread( target=quad_controller, name='quad').start()
#threading.start_new_thread( print_time, ("Thread-2", 4, ) )

print(threading.active_count())
print(threading.enumerate())

#for thread in threading.enumerate():
#    print(thread.daemon)

while 1:
   pass

