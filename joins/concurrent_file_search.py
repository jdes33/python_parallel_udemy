import os
from os.path import isdir, join
from threading import Thread, Lock

mutex = Lock()
matches = []


def file_search(root, filename):
    # recursive search for a file called filename
    print("Searching in:", root)
    child_threads = []
    for file in os.listdir(root):
        full_path = join(root, file) # join's string with os specific seperator
        print(full_path)
        if filename in file:
            # accquire and release when changing shared state (matches)
            mutex.acquire()
            matches.append(full_path)
            mutex.release()
        if isdir(full_path):
            # recursive call, create new thread for each call
            t = Thread(target=file_search, args=([full_path, filename]))
            t.start()
            child_threads.append(t) # (dont join here or it wont be parallel, isntead add to list)

    # ensure all threads created by this function call terminate before this call can finish
    # can imagine as recursive tree unwinding where all brances from a node collapse
    for t in child_threads:
        t.join()



def main():
    t = Thread(target=file_search, args=(["/home/jason/python_parallel_udemy", "letter_counter.py"]))
    t.start()
    t.join()
    for m in matches:
        print("Matched: ", m)

main()