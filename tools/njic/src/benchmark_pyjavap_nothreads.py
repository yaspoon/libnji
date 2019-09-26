#!/usr/bin/python3

import nji
import os
import time
import threading

print("Benchmarking installed njic")

files = []
path = os.path.join(os.getcwd(), "..", "..", "..", "test")
for file in os.listdir(path):
    filename, file_ext = os.path.splitext(file)
    if file_ext == ".nji":
        files.append(os.path.join(path, file))

print("Benchmarking nji.parse using pyjavap {} times".format(len(files)))
start = time.perf_counter()
for f in files:
    nji._internal_parse(open(f), None, True)

end = time.perf_counter()
print("nji.parse with pyjavap took {} seconds".format(end-start))
