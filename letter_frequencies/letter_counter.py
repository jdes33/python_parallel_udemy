import json
from urllib.request import Request, urlopen
import time
from threading import Thread, Lock

finished_count = 0

def count_letters(url, frequency, mutex):
    global finished_count

    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    txt = str(urlopen(req).read())
    
    mutex.acquire()
    for l in txt: 
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1
    finished_count += 1 # increment by 1 every time a thread finishes
    mutex.release()

def main():
    frequency = {}
    mutex = Lock() # will use to protect finished_count variable and frequency dict
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    
    start = time.time()
    for i in range(1000, 1020): 
        Thread(target=count_letters, args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency, mutex)).start()
    
    # check every half a second whether the threads are finished or not
    # there is much better way to do this but for now it'll do
    # acquire mutex since finished count is shared resource
    all_finished = False
    while not all_finished:
        mutex.acquire()
        if finished_count == 20:
            all_finished = True
        mutex.release() 
        time.sleep(0.5) # make sure this after release else nothing can use resource whilst it's sleeping so it defeats the purpose

    end = time.time()
    print(json.dumps(frequency, indent=4))
    print("done, time taken:", end - start)

main()