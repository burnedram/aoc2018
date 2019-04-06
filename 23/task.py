#!/usr/bin/env pipenv-run
import sys
from parse import parse
from collections import defaultdict
from queue import PriorityQueue

from operator import sub, add, itruediv, mul, gt
from functools import reduce
from itertools import starmap, repeat, product, chain

nanobots = list()
for line in sys.stdin:
    x, y, z, r = parse('pos=<{:d},{:d},{:d}>, r={:d}', line)
    nanobots.append(((x, y, z), r))
nanobots.sort()
origin = (0, 0, 0)

def mdist(left, right):
    return sum(map(abs, starmap(sub, zip(left, right))))

def count_in_range_of_bot(points, bot):
    bot, bot_r = bot
    in_range = 0
    for p in points:
        if mdist(p, bot) <= bot_r:
            in_range = in_range + 1
    return in_range

stronkest_bot = max(nanobots, key=lambda pos_r: pos_r[1])
bots_in_range_of_stronkest = count_in_range_of_bot(map(lambda kv: kv[0], nanobots), stronkest_bot) 
print('Task 01: {}'.format(bots_in_range_of_stronkest))

def get_bounding_box(bot):
    bot_pos, bot_r = bot
    bot_zip = tuple(zip(bot_pos, repeat(bot_r)))
    box_min = tuple(starmap(sub, bot_zip))
    box_max = tuple(starmap(add, bot_zip))
    return (box_max, box_min)

def reduce_bounding_boxes(boxes):
    def reducer(state, item):
        zip_max, zip_min = zip(state, item)
        zip_max = tuple(map(max, zip(*zip_max)))
        zip_min = tuple(map(min, zip(*zip_min)))
        return (zip_max, zip_min)
    return reduce(reducer, boxes, next(boxes))

def box_size(box):
    return reduce(mul, starmap(sub, zip(*box)), 1)

def box_center(box):
    return tuple(map(round, starmap(itruediv, zip(starmap(add, zip(*box)), repeat(2)))))

def box_divisions(box):
    if box_size(box) == 1:
        left, right = box
        yield (left, left)
        yield (right, right)
        return
    center = box_center(box)
    points = sorted(product(*zip(*chain(box, (center,)))))
    for i, new_min in enumerate(points):
        for new_max in points[i+1:]:
            if all(starmap(gt, zip(new_max, new_min))):
                yield (new_max, new_min)
                break

def bot_reaches_box(bot, box):
    bot, bot_r = bot
    total = 0
    for box_max, box_min, b in zip(*box, bot):
        if b > box_max:
            total = total + (b - box_max)
        elif b < box_min:
            total = total + (box_min - b)
    return total <= bot_r

def count_bots_reaches_box(bots, box):
    return sum(starmap(bot_reaches_box, zip(bots, repeat(box))))

def count_bots_reaches_pos(bots, pos):
    in_range = 0
    for bot, bot_r in bots:
        if mdist(pos, bot) <= bot_r:
            in_range = in_range + 1
    return in_range

bbox = reduce_bounding_boxes(map(get_bounding_box, nanobots))
p_queue = PriorityQueue()
p_queue.put((0, bbox))
while not p_queue.empty():
    bots_outside, box = p_queue.get()
    left, right = box
    if left == right:
        bots_inside = len(nanobots) - bots_outside
        print('Task 02 found @ {} with {} nanobots: {}'
                .format(left, bots_inside, mdist(origin, left)))
        break
    for box_div in box_divisions(box):
        bots_inside_div = count_bots_reaches_box(nanobots, box_div)
        bots_outside_div = len(nanobots) - bots_inside_div
        p_queue.put((bots_outside_div, box_div))
