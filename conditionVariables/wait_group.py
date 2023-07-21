from threading import Condition

class WaitGroup:
    """
    Class to keep track of several threads in order to know when they are all finished
    """
    wait_group=0
    cv = Condition()

    def add(self, count):
        """Increment wait group counter"""
        self.cv.acquire()
        self.wait_count += count
        self.cv.release()

    def done(self):
        """Decrement wait group counter"""
        self.cv.acquire()
        if self.wait_count > 0:
            self.wait_count -= 1
        if self.wait_count == 0:
            self.cv.notify_all()
        self.cv.release()

    def wait(self):
        """Wait while count above zero (threads still running)"""
        self.cv.acquire()
        # use greater than zero condition as there might be a case where we are notifying that all the threads are done,
        # however just before our thread is woken up another thread comes in and adds more work to the wait group
        while self.wait_count > 0:
            self.cv.wait() # waits here till notified
        self.cv.release()
