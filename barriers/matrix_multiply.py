import time
from random import Random

# multithreaded version
# small speedup maybe but not great due to GIL using one processor and this being cpu bound
# main/parent thread to populate matrices, and then threads, on for each row of matrix, responsible for computation
# two barriers
# 1st barrier: main populates whiles children wait, main waits when done so barrier unlocks
# then all unlock and main waits on second barrier whilst children start doing computatios and each wait on second when done
# When all are waigin on second barrier, it unlocks and process repeats so next matrix can be created and multiplied

from threading import Barrier, Thread

matrix_size = 200
matrix_a = [[0] * matrix_size for a in range(matrix_size)]
matrix_b = [[0] * matrix_size for b in range(matrix_size)]
result = [[0] * matrix_size for r in range(matrix_size)]

random = Random()
# matrix_size as one for each row, plus 1 for parent thread that populates
work_start = Barrier(matrix_size + 1) # to signal that all child threads can start working on their rows 
work_complete = Barrier(matrix_size + 1) # represents that each thread has finished their work

def generate_random_matrix(matrix):
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix[row][col] = random.randint(-5, 5)

def work_out_row(row):
    while True: # infinitle loop as we will compute for multiple matries
        work_start.wait() # waits here till barrier lets through (once matrices populated will be let through since matrix_size+1 threads will be waiting here)
        for col in range(matrix_size):
            for i in range(matrix_size):
                result[row][col] += matrix_a[row][i] + matrix_b[i][col]
        work_complete.wait() #  make thread wait at this barrier as it's done computing

# create thread for each row
for row in range(matrix_size):
    # pass in row number so a thread is responsible for exactly one row throughout program
    Thread(target=work_out_row, args=([row])).start()

start = time.time()
for t in range(10): # perform 10 matrix multiplications
    generate_random_matrix(matrix_a)
    generate_random_matrix(matrix_b)
    result = [[0] * matrix_size for r in range(matrix_size)]
    work_start.wait() #  make main thread wait at work_start barrier (if children are waiting then will be let through)
    work_complete.wait() # make main thread wait at work_complete barrier (once children done with their rows will be let through)

end = time.time()
print("Done, time take: ", end - start)

## EXPLANATION of above code:
## imagine 4x4 matrices
## thus 1 parent/main thread and 4 children one for each row
## There are two barriers work_start and work_complete
## In each case they will need 5 threads to be waiting before barrier drops
## The children all initially will wait at the work_start barrier as shown in the work_out_row function/target
## The main thread will wait there after it's populated the two matrices to be multiplied
## Thus once it's waiting there there will be 5 threads at the barrier and all 5 threads can continue
## In the case of main, the next line tells it to wait at the work_complete barrier.
## In the case of the child threads, they will each have to do the computation for thre row they're responsible for before they can wait at the barrier.
## Once all children done there will be 5 threads waiting at barrier and whole process can restart :)
