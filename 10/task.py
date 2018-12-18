#!/usr/bin/env pipenv-run

import sys
from parse import parse
from collections import defaultdict

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: {} INPUT STOP".format(sys.argv[0]))
    print("\t INPUT: input file")
    print("\t STOP: optional number of chains to stop iteration")
    print("\t       when STOP is provided, the current state of the stars will be printed on exit")
    exit(1)

stop = None
if len(sys.argv) == 3:
    stop = int(sys.argv[2])

stars = defaultdict(list)
with open(sys.argv[1]) as f:
    for line in f:
        x, y, dx, dy = map(int, parse("position=<{},{}> velocity=<{},{}>", line))
        stars[(x, y)].append((dx, dy))
    stars = dict(stars)

def move_stars(stars):
    new_stars = defaultdict(list)
    for (x, y), ds in stars.items():
        for dx, dy in ds:
            new_stars[(x + dx, y + dy)].append((dx, dy))
    return dict(new_stars)

def get_neighbours(star, stars):
    star_x, star_y = star
    for y in range(star_y - 1, star_y + 2):
        for x in range(star_x - 1, star_x + 2):
            if (x, y) in stars:
                yield (x, y)

def find_chains(stars):
    chains = list()
    consumed = set()
    for star in stars:
        if star in consumed:
            continue
        to_check = set()
        to_check.add(star)
        chain = set()
        chain.add(star)
        while to_check:
            star_x, star_y = to_check.pop()
            for y in range(star_y - 1, star_y + 2):
                for x in range(star_x - 1, star_x + 2):
                    if not (x, y) in chain and (x, y) in stars:
                        chain.add((x, y))
                        to_check.add((x, y))
                        consumed.add((x, y))
        chains.append(chain)
    return chains

def print_stars(stars):
    min_x = min(map(lambda star: star[0], stars))
    max_x = max(map(lambda star: star[0], stars))
    min_y = min(map(lambda star: star[1], stars))
    max_y = max(map(lambda star: star[1], stars))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print("#" if (x, y) in stars else ".", end="")
        print()

last_stars = stars
last_chains = find_chains(stars)
seconds = 0
while not len(last_chains) == stop:
    stars = move_stars(stars)
    chains = find_chains(stars)
    if stop is None and (len(chains) > len(last_chains)):
        min_x = min(map(lambda star: star[0], last_stars))
        max_x = max(map(lambda star: star[0], last_stars))
        min_y = min(map(lambda star: star[1], last_stars))
        max_y = max(map(lambda star: star[1], last_stars))
        print("local minima: {}".format(len(last_chains)))
        print("\toccured after {} seconds".format(seconds))
        print("\ttop left: {}".format((min_x, min_y)))
        print("\tbottom right: {}".format((max_x, max_y)))
        print()
    last_chains = chains
    last_stars = stars
    seconds += 1

print_stars(stars)
print()
print("The above starmap occured after {} seconds".format(seconds))
