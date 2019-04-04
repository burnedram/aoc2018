#!/usr/bin/env pipenv-run
from tqdm import tqdm

def run(r2):
    r0 = 0
    with tqdm(total=r2 * r2) as pbar:
        for r3 in range(1, r2 + 1):
            for r5 in range(1, r2 + 1):
                pbar.update(1)
                r1 = r3 * r5
                if r1 == r2:
                    r0 = r0 + r3
    return r0

# Found by running the source a few steps, until it reaches the loops
task01_r2 = 887
task02_r2 = 10551287

print('Task 01: {}'.format(run(task01_r2)))
print('Task 02: {}'.format(run(task02_r2)))
