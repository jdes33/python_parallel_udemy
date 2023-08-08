import time

# unlike threads, cannot use normal queue to send messages between process so use the one from multiprocessing package
from multiprocessing import Process, Queue 

# simple example using queue to pass messages between processes
# basically same as thread version, but using processes and notice change in imports, also of course gotta check if name=main
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

if __name__ == '__main__':
    q = Queue(maxsize=10)
    p1 = Process(target=consumer, args=(q,))
    p2 = Process(target=producer, args=(q,))
    p1.start()
    p2.start()