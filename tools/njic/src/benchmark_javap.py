#!/usr/bin/python3

import nji
import os
import time
import threading

print("Benchmarking installed njic")

files = []

class Benchmark(threading.Thread):
    def __init__(self, javap, nji_file):
        threading.Thread.__init__(self)
        self.javap = javap
        self.nji_file = nji_file
    def run(self):
        nji.parse(open(self.nji_file), None, self.javap)
        print("Finished parsing:{}".format(self.nji_file))

class Busy(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False
    def run(self):
        n = 0
        while not self.stop:
            n = n + 1
        print("Busy done")

count = 16
path = os.path.join(os.getcwd(), "..", "..", "..", "test")
threads = []
for file in os.listdir(path):
    filename, file_ext = os.path.splitext(file)
    if file_ext == ".nji":
        files.append(os.path.join(path, file))

print("Benchmarking nji.parse using javap {} times".format(len(files)))

start = time.perf_counter()
'''
count = int(count / len(files))
if count <= 0:
    count = 1
for i in range(count):
    for f in files:
        thread = Benchmark(True, f)
        thread.start()
        threads.append(thread)
'''
for f in files:
    thread = Benchmark(False, f)
    threads.append(thread)

for t in threads:
    t.start()

b = Busy()
b.start()

for t in threads:
    t.join()

b.stop = True
b.join()

end = time.perf_counter()
print("nji.parse with pyjavap took {} seconds".format(end-start))
