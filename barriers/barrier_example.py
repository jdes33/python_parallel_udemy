
from threading import Barrier, Thread
import time

# simple program illustrating barrier
# barrier makes threads wait there until number of threads
# at barrier is equal to barrier size (then it lets them go and resets internal counter)

barrier = Barrier(2) # set barrier size to 2

def wait_on_barrier(name, time_to_sleep):
    for i in range(3):
        print(name, "running")
        time.sleep(time_to_sleep)
        print(name, "is waiting on barrier", i+1)
        barrier.wait()
    print(name, "is finished")

red = Thread(target=wait_on_barrier, args=["red", 2])
blue = Thread(target=wait_on_barrier, args=["blue", 5])
red.start()
blue.start()

##  note: you can also abort barriers if needed (throws barrier broken exception)
#  abort barrier after 8 seconds
#   print("Aborting barrier")
#   barrier.abort()
