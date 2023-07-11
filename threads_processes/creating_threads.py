import time
from threading import Thread

def do_work():
    print("Starting work")
    time.sleep(1)
    print("finished work")

# # this is example of cpu bound, if you uncomment you see they dont all finish at same time 
# # he did this to proves threads don't use more than one processor
# # you can even examine cpu util whilst running and you will see not all used
# def do_work():
#     print("Starting work")
#     i = 0
#     for _ in range(20000000):
#         i += 1
#     print("finished work")


for _ in range(5):
    t = Thread(target=do_work, args=())
    t.start()
    #do_work()
