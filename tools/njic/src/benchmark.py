#!/usr/bin/python

import nji
import os
import time
import threading

print("Benchmarking installed njic")

class Benchmark(threading.Thread):
    def __init__(self, javap):
        threading.Thread.__init__(self)
        self.javap = javap
    def run(self):
        nji.parse(open(path), None, self.javap)

thread_count = 8
count = 100
#path = os.path.join(os.getcwd(), 'thread.nji')
path = os.path.join('/home/brock/code/libnji/test', 'thread.nji')
threads = []
print("Benchmarking default nji.parse shelling out to javap {} times".format(count))
start = time.perf_counter()
i = 0
while i < count:
    threads = []
    for j in range(thread_count):
        thread = Benchmark(False)
        thread.start()
        threads.append(thread)

        for t in threads:
            t.join()
    i += thread_count
    print("{} threads done".format(i))

end = time.perf_counter()
print("Default nji.parse took {} seconds".format(end-start))

print("Benchmarking nji.parse using pyjavap {} times".format(count))
start = time.perf_counter()
i = 0
while i < count:
    threads = []
    for j in range(thread_count):
        thread = Benchmark(False)
        thread.start()
        threads.append(thread)

        for t in threads:
            t.join()
    i += thread_count
    print("{} threads done".format(i))
end = time.perf_counter()
print("nji.parse with pyjavap took {} seconds".format(end-start))
