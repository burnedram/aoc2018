#!/usr/bin/python3

import sys
from parse import parse
from collections import deque

(n_players, n_marbles) = map(int, parse("{} players; last marble is worth {} points", sys.stdin.read()))

circle = deque([0])
players = deque([0]*n_players)

for marble in range(1, n_marbles + 1):
    if marble % 23 == 0:
        players[0] += marble
        circle.rotate(7)
        players[0] += circle.pop()
        circle.rotate(-1)
    else:
        circle.rotate(-1)
        circle.append(marble)
    players.rotate()

print("Highscore: {}".format(max(players)))
