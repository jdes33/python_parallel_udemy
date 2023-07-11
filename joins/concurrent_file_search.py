import os

from os.path import isdir, join

matches = []

def file_search(root, filename):
    # recursive search for a file called filename
    print("Searching in:", root)
    for file in os.listdir(root):
        full_path = join(root, file) # join's string with os specific seperator
        print(full_path)
        if filename in file:
            matches.append(full_path)
        if isdir(full_path):
            file_search(full_path, filename)

def main():
    file_search("/home/jason/python_parallel_udemy", "letter_counter.py")
    for m in matches:
        print("Matched: ", m)

main()