import multiprocessing
from multiprocessing import Process

def do_work():
    print("Starting work")
    i = 0
    for _ in range(20000000):
        i += 1
    print("finished work")

# when using python processes, 
# because they are running in seperate python interpreters,
# they will all execute the code that you leave outside functions, 
# so use the if statement trick to check if we're the main or not
# if you examine cpu util whilst running you will see all cores used
# also notice they all finish about the same time
if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    for _ in range(5):
        p = Process(target=do_work, args=())
        p.start()

