import json
from urllib.request import Request, urlopen
import time
from threading import Thread

finished_count = 0

def count_letters(url, frequency):
    req = Request(
        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    #response = urllib.request.urlopen(url)
    txt = str(urlopen(req).read())
    #txt = str(response.read())
    for l in txt: 
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1
    global finished_count
    finished_count += 1 # increment by 1 every time a thread finishes


def main():
    frequency = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    
    start = time.time()
    for i in range(1000, 1020): 
        Thread(target=count_letters, args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency)).start()
    
    # check every half a second whether the threads are finished or not
    # there is much better way to do this but for now it'll do
    while finished_count < 20:
        time.sleep(0.5)
    
    end = time.time()
    print(json.dumps(frequency, indent=4))
    print("done, time taken:", end - start)

main()

## NEED TO FINISH UP CODE BY USING VIDEO 14