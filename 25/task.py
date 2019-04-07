#!/usr/bin/env pipenv-run
import sys
from parse import parse

from operator import sub 
from itertools import starmap

def mdist(left, right):
    return sum(map(abs, starmap(sub, zip(left, right))))

origin = (0, 0, 0, 0)
spacetime = set()
for line in sys.stdin:
    x, y, z, t = parse('{:d},{:d},{:d},{:d}', line)
    spacetime.add((x, y, z, t))

def sort_spacetime(spacetime):
    def sorter(spacetime):
        global origin
        spacetime = spacetime.copy()
        last_pos = max(spacetime, key=lambda pos: mdist(origin, pos))
        spacetime.remove(last_pos)
        yield last_pos
        while spacetime:
            last_pos = min(spacetime, key=lambda pos: mdist(last_pos, pos))
            spacetime.remove(last_pos)
            yield last_pos
    return list(sorter(spacetime))

def find_constellations(spacetime):
    spacetime = spacetime.__iter__()
    constellation = [next(spacetime)]
    result = [constellation]
    for pos in spacetime:
        new_constellation = True
        for pos_in_constellation in constellation:
            if mdist(pos_in_constellation, pos) <= 3:
                new_constellation = False
                break
        if new_constellation:
            constellation = list()
            result.append(constellation)
        constellation.append(pos)
    return result

def join_constellations(constellations):
    did_something = False
    i = 0
    while i < len(constellations):
        left = constellations[i]
        j = i+1
        while j < len(constellations):
            right = constellations[j]
            joined = False
            for left_pos in left:
                for right_pos in right:
                    if mdist(left_pos, right_pos) <= 3:
                        left.extend(right)
                        joined = True
                        break
                if joined:
                    break
            if joined:
                did_something = True
                del constellations[j]
                j = j - 1
            j = j + 1
        i = i + 1
    return did_something

sorted_spacetime = sort_spacetime(spacetime)
constellations = find_constellations(sorted_spacetime)
while join_constellations(constellations):
    pass
print('Task 01: {}'.format(len(constellations)))
