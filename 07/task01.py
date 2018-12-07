#!/usr/bin/python3

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

while len(ready_steps) > 0:
    step = ready_steps.pop(0)
    print(step, end="")
    modified = False
    for reverse in reverse_steps[step]:
        begin = steps[reverse]
        begin.remove(step)
        if len(begin) == 0:
            modified = True
            ready_steps.append(reverse)
    if modified:
        ready_steps.sort()
print()
