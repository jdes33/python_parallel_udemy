from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection # Don't need this: purely for documentation/autocomplete purposes
import time

# Example of using Pipe for message passing between processes
# Notice there are two ends of the pipe, we call them end a and b
# if we recv from end a, then we are trying to read something send from end b
# (... and vice versa - we can't recv a message that we have send from our end)
# In this example end a send pings messages and recieves pong messages
# whereas end b sends pong messages and recieves ping messages

def ping(pipe_conn: Connection):
    while(True):
        # (unlike queues, in pipe you can both send and recieve from the same process as shown here)
        pipe_conn.send(["Ping", time.time()]) # send ping and timestamp (put in list to send two things in one go)
        pong = pipe_conn.recv() # recieve one message on the pipe
        print(pong)
        time.sleep(1)

def pong(pipe_conn: Connection):
    while(True):
        ping = pipe_conn.recv()
        print(ping)
        time.sleep(1)
        pipe_conn.send(["Pong", time.time()])


if __name__ == '__main__':
    # (note the type of each pipe_end will be Connection)
    pipe_end_a, pipe_end_b = Pipe() # a pipe has two ends, the creation of Pipe returns a tuple so we can assign variable to each end
    Process(target=ping, args=(pipe_end_a,)).start()
    Process(target=pong, args=(pipe_end_b,)).start()