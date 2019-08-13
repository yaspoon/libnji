#!/usr/bin/python

import nji
import os
import time

print("Benchmarking installed njic")

count = 100
print("Benchmarking default nji.parse shelling out to javap {} times".format(count))
start = time.perf_counter()
for i in range(count):
    nji.parse(open(os.path.join(os.getcwd(), 'thread.nji'))
, None, False)
end = time.perf_counter()
print("Default nji.parse took {} seconds".format(end-start))

print("Benchmarking nji.parse using pyjavap {} times".format(count))
start = time.perf_counter()
for i in range(count):
    nji.parse(open(os.path.join(os.getcwd(), 'thread.nji'))
, None, True)
end = time.perf_counter()
print("nji.parse with pyjavap took {} seconds".format(end-start))
