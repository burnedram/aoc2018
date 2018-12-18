#!/usr/bin/env pipenv-run

import sys
from parse import parse
from collections import defaultdict

steps = defaultdict(set)
reverse_steps = defaultdict(set)

for line in sys.stdin:
    (before, begin) = parse("Step {} must be finished before step {} can begin.", line)
    steps[before] # touch
    steps[begin].add(before)
    reverse_steps[before].add(begin)

ready_steps = list(map(lambda kv: kv[0], filter(lambda kv: len(kv[1]) == 0, steps.items())))
ready_steps.sort()

base_time = 60
idle_workers = 1 + 5
workers = []

total_time = 0
while len(workers) > 0 or len(ready_steps) > 0:
    while idle_workers > 0 and len(ready_steps) > 0:
        step = ready_steps.pop(0)
        workers.append((base_time + (ord(step) - ord('A') + 1), step))
        idle_workers -= 1

    workers.sort()
    done_in = workers[0][0]
    total_time += done_in
    workers = list(map(lambda x: (x[0] - done_in, x[1]), workers))

    modified = False
    while len(workers) > 0 and workers[0][0] == 0:
        step = workers.pop(0)[1]
        idle_workers += 1
        print(step, end="")
        for reverse in reverse_steps[step]:
            begin = steps[reverse]
            begin.remove(step)
            if len(begin) == 0:
                modified = True
                ready_steps.append(reverse)
    if modified:
        ready_steps.sort()
print()
print("Total time: {}".format(total_time))
