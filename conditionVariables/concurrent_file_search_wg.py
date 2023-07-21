# modified concurrent file search with joins file to use wait groups instead
import os
from os.path import isdir, join
from threading import Thread, Lock

from conditionVariables.wait_group import WaitGroup

mutex = Lock()
matches = []


def file_search(root, filename, wait_group):
    # recursive search for a file called filename
    print("Searching in:", root)
    for file in os.listdir(root):
        full_path = join(root, file) # join's string with os specific seperator
        print(full_path)
        if filename in file:
            mutex.acquire()
            matches.append(full_path)
            mutex.release()
        if isdir(full_path):
            # recursive call, create new thread for each call
            wait_group.add(1) # increment wait group counter
            t = Thread(target=file_search, args=([full_path, filename, wait_group]))
            t.start()
    wait_group.done() # decrement wait group counter

def main():
    wait_group = WaitGroup()
    wait_group.add(1) # incremenent wait group counter everytime new thread created
    t = Thread(target=file_search, args=(["/home/jason/python_parallel_udemy", "letter_counter.py", wait_group]))
    t.start()
    wait_group.wait() # will wait here till wait group counter reaches zero
    for m in matches:
        print("Matched: ", m)

main()