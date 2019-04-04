#!/usr/bin/env pipenv-run

from isqrt import isqrt

# The program described in input.txt calculates the sum of all x which satisfies x*y == c
# Where
#   c is an integer constant, stored in register #2,
#   0 > x <= c, integer
#   0 > y <= c, integer
# The result is stored in register #0, which is what the question asks for

def run(c):
    # c is always divisable by 1, i.e. 1*c == c and c*1 == c
    n = c + 1
    step = 2
    if c % 2 == 0:
        # if c is divisible by 2, then 2*(c//2) == c and (c//2)*2 == c
        n = n + 2 + (c // 2)
        # this also means that it could be divisable by other even numbers
        step = 1
    # check all integers larger than 2, but smaller or equal to sqrt(c),
    # since sqrt(c)*sqrt(c) is the "largest" solution
    for i in range(3, isqrt(c), step):
        if c % i == 0:
            n = n + i + (c // i)
    return n

# Found by running the source a few steps, until it reaches the loops
task01_c = 887
task02_c = 10551287

print('Task 01: {}'.format(run(task01_c)))
print('Task 02: {}'.format(run(task02_c)))
