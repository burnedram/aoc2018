#!/usr/bin/python3

import sys
from functools import reduce
from operator import add
from operator import sub
from math import ceil

cutoff = 10000

coords = list()
for line in sys.stdin.read().splitlines():
    (x, y) = map(int, line.split(", "))
    coords.append((x, y))
min_x = min(map(lambda xy: xy[0], coords))
max_x = max(map(lambda xy: xy[0], coords))
min_y = min(map(lambda xy: xy[1], coords))
max_y = max(map(lambda xy: xy[1], coords))

(centroid_x, centroid_y) = map(round, map(lambda x: x/len(coords), reduce(lambda coord1, coord2: map(add, coord1, coord2), coords)))

def get_dist(x, y):
    dist = 0
    for xy in coords:
        dist += sum(map(abs, map(sub, xy, (x, y))))
        if dist >= cutoff:
            return dist
    return dist

centroid_dist = get_dist(centroid_x, centroid_y)
dist_to_go = cutoff - centroid_dist
outside_max_dist = ceil(dist_to_go / len(coords))
outside_max_x = max_x + outside_max_dist
outside_min_x = min_x - outside_max_dist
outside_max_y = max_y + outside_max_dist
outside_min_y = min_y - outside_max_dist

def divide_conquer_x(start_x, step_x, y, op):
    dist = get_dist(op(start_x, step_x), y)
    if dist < cutoff:
        return op(start_x, step_x)
    step_x = ceil(step_x / 2)
    while True:
        dist = get_dist(op(start_x, step_x), y)
        if dist < cutoff:
            start_x = op(start_x, step_x)
        if step_x == 1:
            break
        step_x = ceil(step_x / 2)
    return start_x

def divide_conquer_y(x, start_y, step_y, op):
    dist = get_dist(x, op(start_y, step_y))
    if dist < cutoff:
        return op(start_y, step_y)
    step_y = ceil(step_y / 2)
    while True:
        dist = get_dist(x, op(start_y, step_y))
        if dist < cutoff:
            start_y = op(start_y, step_y)
        if step_y == 1:
            break
        step_y = ceil(step_y / 2)
    return start_y

actual_max_x = divide_conquer_x(centroid_x, outside_max_x - centroid_x, centroid_y, add)
actual_min_x = divide_conquer_x(centroid_x, centroid_x - outside_min_x, centroid_y, sub)
actual_max_y = divide_conquer_y(centroid_x, centroid_y, outside_max_y - centroid_y, add)
actual_min_y = divide_conquer_y(centroid_x, centroid_y, centroid_y - outside_min_y, sub)

region_size = 1 # 1 since centroid is in region
region_size += actual_max_x - centroid_x # right side of x-axis
region_size += centroid_x - actual_min_x # left side of x-axis
region_size += actual_max_y - centroid_y # max side of y-axis
region_size += centroid_y - actual_min_y # min side of y-axis

flood_max_y = actual_max_y
flood_min_y = actual_min_y
for x in range(centroid_x + 1, actual_max_x + 1, 1):
    # right max quadrant
    flood_max_y = divide_conquer_y(x, centroid_y, flood_max_y - centroid_y, add)
    region_size += flood_max_y - centroid_y

    # right min quadrant
    flood_min_y = divide_conquer_y(x, centroid_y, centroid_y - flood_min_y, sub)
    region_size += centroid_y - flood_min_y

flood_max_y = actual_max_y
flood_min_y = actual_min_y
for x in range(centroid_x - 1, actual_min_x - 1, -1):
    # left max quadrant
    flood_max_y = divide_conquer_y(x, centroid_y, flood_max_y - centroid_y, add)
    region_size += flood_max_y - centroid_y

    # left min quadrant
    flood_min_y = divide_conquer_y(x, centroid_y, centroid_y - flood_min_y, sub)
    region_size += centroid_y - flood_min_y

print(region_size)
