import time
from queue import Queue

from threading import Thread

# simple example using queue to pass messages between threads
# We put no sleep in producer so it will quickly fill up queue's capacity with messages
# then consumer will take one message from queue every second
# every time consumer takes a message, a space is made free on queue and producer can send another message

def consumer(q: Queue):
    while(True):
        txt = q.get() # blocks while queue is empty
        print(txt)
        time.sleep(1)

def producer(q: Queue):
    while(True):
        q.put("Hello there") # blocks till free slot on queue available
        print("Message Sent")

q = Queue(maxsize=10)
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()