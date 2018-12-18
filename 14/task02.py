#!/usr/bin/env pipenv-run

import sys
from collections import deque

recipes = deque(map(int, next(sys.stdin).strip()))
left_of = deque(maxlen=len(recipes))

scoreboard = [3, 7]
elfs = set([0, 1])

def print_scoreboard(scoreboard, elfs):
    for i, entry in enumerate(scoreboard):
        print("{}{}{}".format("[" if i in elfs else " ", entry, "]" if i in elfs else " "), end="")
    print()

#print_scoreboard(scoreboard, elfs)
while True:
    score = sum(map(lambda elf: scoreboard[elf], elfs))
    for ch in map(int, str(score)):
        scoreboard.append(ch)
        left_of.append(ch)
        if recipes == left_of:
            print(len(scoreboard) - len(recipes))
            exit(0)
    new_elfs = set()
    for elf in elfs:
        new_elfs.add((elf + 1 + scoreboard[elf]) % len(scoreboard))
    elfs = new_elfs
    #print_scoreboard(scoreboard, elfs)
