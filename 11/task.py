#!/usr/bin/python3

import sys

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

grid = dict()
for y in range(1, grid_size + 1):
    for x in range(1, grid_size + 1):
        grid[(x, y)] = power_level(grid_sn, (x, y))

def all_windows(grid, grid_size, window_size):
    if len(sys.argv) < 3:
        print("{:.2f}%".format(100 * window_size / grid_size))
    last_lvl = 0
    for y in range(1, 1 + window_size - 1):
        for x in range(1, 1 + window_size - 1):
            last_lvl += grid[(x, y)]
    for window_y in range(1, grid_size + 1 - window_size + 1):
        for x in range(1, 1 + window_size - 1):
            last_lvl += grid[(x, window_y + window_size -1)]
        lvl = last_lvl
        for x in range(1, 1 + window_size - 1):
            last_lvl -= grid[(x, window_y)]
        for window_x in range(1, grid_size + 1 - window_size + 1):
            for y in range(window_y, window_y + window_size):
                lvl += grid[(window_x + window_size - 1, y)]
            yield (window_x, window_y, window_size, lvl)
            for y in range(window_y, window_y + window_size):
                lvl -= grid[(window_x, y)]

window_x, window_y, window_size, lvl = max(map(lambda window_size: max(all_windows(grid, grid_size, window_size), key=lambda w: w[3]), window_sizes), key=lambda candidate: candidate[3])
print("largest window of size {}x{} found @ ({}, {}): {}".format(window_size, window_size, window_x, window_y, lvl))
