import multiprocessing
from multiprocessing import Process

import time

# (unlike threads, processes have their own memory spaces)
# program to illustrate how to share memory between processes
# We make an array in shared memory and modify it in main process,
# the other process just keeps printing the array and we can see that it has been modified as expected.

def print_array_contents(array):
    while True:
        print(*array, sep=", ")
        time.sleep(1)


# recall we need to check if main when using processes
if __name__ == '__main__':
    ## arr = [-1] * 10 # this won't work as a copy of the list is made when we spawn the child process, so when the main process modifies this one, it doesnt affect the copy
    # thus we create an array in shared memory using multiprocessing library
    # here i is for the type of data (int)
    arr = multiprocessing.Array('i', [-1] * 10) # lock=True by default meaning every access to the array in synchronised (one process can access at time, just like how we did with acquiring a mutex lock, modifying array and releasing it)

    p = Process(target=print_array_contents, args=([arr]))
    p.start()
    for j in range(10):
        time.sleep(2)
        for i in range(10):
            arr[i] = j