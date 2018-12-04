#!/usr/bin/python3

import sys
from models import Entry
from parse import parse
from collections import defaultdict

class Guard:
    def __init__(self, id):
        self.id = id

guards = dict()
current_guard = None
feel_asleep = None

for line in sys.stdin:
    entry = Entry(line)
    if entry.action.startswith("Guard"):
        current_guard = int(parse("Guard #{} begins shift", entry.action)[0])
    elif entry.action == "falls asleep":
        feel_asleep = entry.minute
    elif entry.action == "wakes up":
        if not current_guard in guards:
            guards[current_guard] = defaultdict(int)
        for minute in range(feel_asleep, entry.minute):
            guards[current_guard][minute] += 1

for guard in sorted(guards.keys()):
    print("#{}, total: {}".format(guard, sum(guards[guard].values())))
    for wut in sorted(guards[guard].keys()):
        print("\t{}: {}".format(wut, guards[guard][wut]))

print("Strategy 1")
strat1_guard_id = max(guards.keys(), key=lambda guard: sum(guards[guard].values()))
strat1_guard = guards[strat1_guard_id];
print("\tMost asleep guard: #{}".format(strat1_guard_id))
strat1_minute = max(strat1_guard.keys(), key=lambda minute: strat1_guard[minute])
print("\tMost asleep at minute: {}".format(strat1_minute))
print("\tAnswer: {}".format(strat1_guard_id * strat1_minute))
print()

print("Strategy 2")
strat2_guard_id = max(guards.keys(), key=lambda guard: max(guards[guard].values()))
strat2_guard = guards[strat2_guard_id]
print("\tMost asleep guard: #{}".format(strat2_guard_id))
strat2_minute = max(strat2_guard.keys(), key=lambda minute: strat2_guard[minute])
print("\tMost asleep at minute: {}".format(strat2_minute))
print("\tAnswer: {}".format(strat2_guard_id * strat2_minute))
print()
