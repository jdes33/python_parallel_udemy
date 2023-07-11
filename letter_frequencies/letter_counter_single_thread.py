import json
from urllib.request import Request, urlopen
import time

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


def main():
    frequency = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    
    start = time.time()
    for i in range(1000, 1020): 
        count_letters(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency)
        print(f"done {i}")
    end = time.time()
    print(json.dumps(frequency, indent=4))
    print("done, time taken:", end - start)

main()
