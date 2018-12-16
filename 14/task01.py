#!/usr/bin/python3

import sys

recipes = int(next(sys.stdin))

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
        if len(scoreboard) == recipes + 10:
            print("".join(map(str, scoreboard[-10:])))
            exit(0)
    new_elfs = set()
    for elf in elfs:
        new_elfs.add((elf + 1 + scoreboard[elf]) % len(scoreboard))
    elfs = new_elfs
    #print_scoreboard(scoreboard, elfs)
