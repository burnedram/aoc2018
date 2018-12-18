#!/usr/bin/env pipenv-run

import sys
from operator import sub

coords = dict()
for line in sys.stdin.read().splitlines():
    (x, y) = map(int, line.split(", "))
    coords[(x, y)] = 0
min_x = min(map(lambda xy: xy[0], coords.keys()))
max_x = max(map(lambda xy: xy[0], coords.keys()))
min_y = min(map(lambda xy: xy[1], coords.keys()))
max_y = max(map(lambda xy: xy[1], coords.keys()))

def get_closest_coords(x, y):
    closest_coords = list()
    min_dist = None
    for xy in coords.keys():
        dist = sum(map(abs, map(sub, xy, (x, y))))
        if min_dist is None or dist < min_dist:
            closest_coords.clear()
            closest_coords.append(xy)
            min_dist = dist
        elif dist == min_dist:
            closest_coords.append(xy)
    return closest_coords

for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        closest_coords = get_closest_coords(x, y)
        if len(closest_coords) == 1:
            coords[closest_coords[0]] += 1

infinite = set()
for x in range(min_x - 1, max_x + 2):
    closest_coords = get_closest_coords(x, min_y - 1)
    for xy in closest_coords:
        infinite.add(xy)
    closest_coords = get_closest_coords(x, max_y + 1)
    for xy in closest_coords:
        infinite.add(xy)
for y in range(min_y - 1, max_y + 2):
    closest_coords = get_closest_coords(min_x - 1, y)
    for xy in closest_coords:
        infinite.add(xy)
    closest_coords = get_closest_coords(max_x + 1, y)
    for xy in closest_coords:
        infinite.add(xy)
for xy in infinite:
    del coords[xy]

print(max(coords.values()))
