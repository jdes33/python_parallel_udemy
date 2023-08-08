import time
from random import Random

# (ADAPTED from multithreaded version in barriers directory to instead use multiple processes)
# (in multithreaded took 32 seconds, but here with 8 processors took just 10 seconds)
# multiprocessing version 
# unlike multithreaded, we actually get nice speedup as we are now using multiple processors
# main/parent process to populate matrices, and then child processes, each for a portion of the rows of the matrix, responsible for computation (linear combination)
# two barriers
# 1st barrier: main populates whiles children wait, main waits when done so barrier unlocks
# then all unlock and main waits on second barrier whilst children start doing computatios and each wait on second when done
# When all are waiting on second barrier, it unlocks and process repeats so next matrix can be created and multiplied

import multiprocessing
from multiprocessing import Barrier, Process # ! import Barrier from multiprocessing this time: works same as thread one, but for processes

process_count = 8 # processes are heavyweight unlike threads so shouldn't create one for each row, I use 8 as I have 8 processors, and will let each deal with a quarter of the rows
matrix_size = 200
matrix_a = [[0] * matrix_size for a in range(matrix_size)]
matrix_b = [[0] * matrix_size for b in range(matrix_size)]
result = [[0] * matrix_size for r in range(matrix_size)]

random = Random()

def generate_random_matrix(matrix):
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix[row * matrix_size + col] = random.randint(-5, 5)

# pass in process id 
# unlike in multithreaded, we have to pass in the matrices and barriers as well as processes don't share memory (each process has its own memory space), so we pass them in as we wanna share em
def work_out_some_rows(id, matrix_a, matrix_b, result, work_start, work_complete):
    while True: # infinitle loop as we will compute for multiple matries
        work_start.wait() # waits here till barrier lets through
        for row in range(id, matrix_size, process_count): # start at process id and takes step of number of processes, so that each process is reposibly for equal amount of rows
            for col in range(matrix_size):
                for i in range(matrix_size):
                    # use formula to map from 2d array to 1d
                    result[row * matrix_size + col] += matrix_a[row * matrix_size + i] + matrix_b[i * matrix_size + col]
        work_complete.wait() #  make process wait at this barrier as it's done computing for rows its respnosible for

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    # process_count as one for each process, plus 1 for main/parent processes that populates
    work_start = Barrier(process_count + 1) # to signal that all child processes can start working on their rows 
    work_complete = Barrier(process_count + 1) # represents that each processes has finished their work
    
    # create each of the necessary matrices in shared memory so the processes can access em
    # since each of the processes are writing in different rows of the result (and just reading from matrices a and b),
    #  we dont't have to worry about locking, so set lock which is default to true to false
    # this makes it a little faster as it doesnt have to lock every time a process needs to read or modify shared memory space
    # note: python only allows to create 1d arrays in shared memory so we will have to map row and column number to index of 1d array
    matrix_a = multiprocessing.Array('i', [0] * (matrix_size * matrix_size), lock=False)
    matrix_b = multiprocessing.Array('i', [0] * (matrix_size * matrix_size), lock=False)
    result = multiprocessing.Array('i', [0] * (matrix_size * matrix_size), lock=False)

    # create processes, each responsible for matrix_size/process_count number number of rows
    for p in range(process_count):
        Process(target=work_out_some_rows, args=([p, matrix_a, matrix_b, result, work_start, work_complete])).start()

    start = time.time()
    for t in range(10): # perform 10 matrix multiplications
        generate_random_matrix(matrix_a)
        generate_random_matrix(matrix_b)

        # need to reset result matrix to zero, but since we're using shared mem space we cant just assign new vaue to it
        # so we go through each element and set to zero
        for i in range(matrix_size * matrix_size):
            result[i] = 0
        work_start.wait() #  make main thread wait at work_start barrier (if children are waiting then will be let through)
        work_complete.wait() # make main thread wait at work_complete barrier (once children done with their rows will be let through)

    end = time.time()
    print("Done, time take: ", end - start)

## EXPLANATION of above code:
## imagine 6x6 matrices and three child processes
## thus 4 processes in total as we have main process too
## There are two barriers work_start and work_complete
## In each case they will need 4 processes to be waiting before barrier drops
## The children all initially will wait at the work_start barrier as shown in the work_out_row function/target
## The main process will wait there after it's populated the two matrices to be multiplied
## Thus once it's waiting there there will be 4 processes at the barrier and all 4 processes can continue
## In the case of main, the next line tells it to wait at the work_complete barrier.
## In the case of the child processes, they will each have to do the computation for thre rows they're responsible for before they can wait at the barrier.
## Once all children done there will be 4 processes waiting at barrier and whole process can restart :)
