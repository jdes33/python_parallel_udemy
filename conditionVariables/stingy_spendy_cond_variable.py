from threading import Thread, Condition


class StingySpeedy:
    money = 100
    cv = Condition() # create conditional variable (like lock but with additional operations)

    def stingy(self):
        for _ in range(1000000):
            self.cv.acquire() # acquire and release as usual
            self.money += 10
            self.cv.notify() # notify after changing money
            self.cv.release()
        print("Stingy Done")

    def spendy(self):
        for _ in range(500000):
            self.cv.acquire()
            while self.money < 20: # check and make wait again if still true
                # WAIT RELEASES THE LOCK THAT'S BEEN ACQUIRED BY SPENDY, SO STRINGY CAN ACCESS RESOURCE
                self.cv.wait() # wait until notified or timeout occurs (can pass in timeout arg too if wanted, but we'll make wait unlimited)
            self.money -= 20
            if self.money < 0: # should never be true if implemented correctly
                print("Money in bank", self.money)
            self.cv.release()
        print("Spendy Done")

ss = StingySpeedy()

st = Thread(target=ss.stingy, args=())
sp = Thread(target=ss.spendy, args=())

st.start()
sp.start()

st.join()
sp.join()

print("Money in the end", ss.money)