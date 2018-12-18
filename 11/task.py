#!/usr/bin/env pipenv-run

import sys
from collections import defaultdict

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: {} INPUT SIZE".format(sys.argv[0]))
    print("\t INPUT: input file")
    print("\t SIZE: (optional) size of squares to look at")
    exit(1)

grid_size = 300
window_sizes = None
if len(sys.argv) == 3:
    window_sizes = [int(sys.argv[2])]
else:
    window_sizes = list(range(1, grid_size + 1))

with open(sys.argv[1]) as f:
    grid_sn = int(f.read())

def power_level(grid_sn, cell_pos):
    x, y = cell_pos
    rack_id = x + 10
    return (((((rack_id * y) + grid_sn) * rack_id) // 100) % 10) - 5

grid = defaultdict(int)
for y in range(1, grid_size + 1):
    for x in range(1, grid_size + 1):
        grid[(x, y)] = power_level(grid_sn, (x, y))

summed = defaultdict(int)
for y in range(1, grid_size + 1):
    for x in range(1, grid_size + 1):
        summed[(x, y)] = grid[(x, y)] + summed[(x, y - 1)] + summed[(x - 1, y)] - summed[(x - 1, y - 1)]

def all_windows(summed, grid_size, window_size):
    for y in range(1, grid_size + 1 - window_size + 1):
        for x in range(1, grid_size + 1 - window_size + 1):
            lvl = summed[(x + window_size - 1, y + window_size - 1)] + summed[(x - 1, y - 1)] - summed[(x + window_size - 1, y - 1)] - summed[(x - 1, y + window_size - 1)]
            yield (x, y, window_size, lvl)

window_x, window_y, window_size, lvl = max(map(lambda window_size: max(all_windows(summed, grid_size, window_size), key=lambda w: w[3]), window_sizes), key=lambda w: w[3])
print("largest window of size {}x{} found @ ({}, {}): {}".format(window_size, window_size, window_x, window_y, lvl))
