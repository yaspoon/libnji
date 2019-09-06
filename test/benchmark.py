#!/usr/bin/python

import nji
import os
import time
import threading

print("Benchmarking installed njic")

class Benchmark(threading.Thread):
    def __init__(self, javap):
        self.javap = javap
    def run(self):
        nji.parse(open(path), None, self.javap)

count = 100
path = os.path.join(os.getcwd(), 'thread.nji')
threads = []
print("Benchmarking default nji.parse shelling out to javap {} times".format(count))
start = time.perf_counter()
for i in range(count):
    thread = Benchmark(False)
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()
end = time.perf_counter()
print("Default nji.parse took {} seconds".format(end-start))

print("Benchmarking nji.parse using pyjavap {} times".format(count))
start = time.perf_counter()
for i in range(count):
    thread = Benchmark(True)
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()
end = time.perf_counter()
print("nji.parse with pyjavap took {} seconds".format(end-start))
