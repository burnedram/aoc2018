#!/usr/bin/python3

import sys
from functools import reduce
from operator import add
from operator import sub
import itertools

coords = list()
for line in sys.stdin.read().splitlines():
    (x, y) = map(int, line.split(", "))
    coords.append((x, y))
min_x = min(map(lambda xy: xy[0], coords))
max_x = max(map(lambda xy: xy[0], coords))
min_y = min(map(lambda xy: xy[1], coords))
max_y = max(map(lambda xy: xy[1], coords))

centroid = tuple(map(round, map(lambda x: x/len(coords), reduce(lambda coord1, coord2: map(add, coord1, coord2), coords))))
cutoff = 10000 - 1
def get_dist(x, y):
    dist = 0
    for xy in coords:
        dist += sum(map(abs, map(sub, xy, (x, y))))
        if dist > cutoff:
            return dist
    return dist

region_size = 0
for x_offset in itertools.count(0):
    dist = get_dist(centroid[0] + x_offset, centroid[1])
    if dist > cutoff:
        break
    region_size += 1
    # upper right quadrant
    for y_offset in itertools.count(1):
        dist = get_dist(centroid[0] + x_offset, centroid[1] + y_offset)
        if dist > cutoff:
            break
        region_size +=1
    # lower right quadrant
    for y_offset in itertools.count(1):
        dist = get_dist(centroid[0] + x_offset, centroid[1] - y_offset)
        if dist > cutoff:
            break
        region_size +=1
for x_offset in itertools.count(1):
    dist = get_dist(centroid[0] - x_offset, centroid[1])
    if dist > cutoff:
        break
    region_size += 1
    # upper left quadrant
    for y_offset in itertools.count(1):
        dist = get_dist(centroid[0] - x_offset, centroid[1] + y_offset)
        if dist > cutoff:
            break
        region_size +=1
    # lower left quadrant
    for y_offset in itertools.count(1):
        dist = get_dist(centroid[0] - x_offset, centroid[1] - y_offset)
        if dist > cutoff:
            break
        region_size +=1
print(region_size)
