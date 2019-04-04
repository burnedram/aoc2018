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

print('Task 01: {}'.format(run(887)))
print('Task 02: {}'.format(run(10551287)))
