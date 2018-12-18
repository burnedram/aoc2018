#!/usr/bin/env pipenv-run

import sys

class Node:
    def __init__(self):
        self.children = list()
        self.metadata = list()
        self.sum_metadata = None
        self.value = None

    def calc(self):
        self.sum_metadata = sum(self.metadata) + sum(map(lambda x: x.sum_metadata, self.children))

        if not self.children:
            self.value = sum(self.metadata)
        else:
            self.value = sum(map(lambda x: self.children[x - 1].value if x > 0 and x - 1 < len(self.children) else 0, self.metadata))

nodes = list()
n_children = list()
n_metadata = list()

def consume_n_children(n):
    global count
    node = Node()
    if nodes:
        nodes[-1].children.append(node)
    nodes.append(node)
    n_children.append(n)
    return consume_n_metadata

def consume_n_metadata(n):
    n_metadata.append(n)
    return consume_child

def consume_child(n):
    nc = n_children.pop()
    if nc == 0:
        return consume_metadata(n)
    n_children.append(nc - 1)
    return consume_n_children(n)

def consume_metadata(n):
    nm = n_metadata.pop()
    if nm == 0:
        nodes.pop().calc()
        return consume_child(n)
    nodes[-1].metadata.append(n)
    n_metadata.append(nm - 1)
    return consume_metadata

operation = consume_n_children
for n in map(int, sys.stdin.read().split()):
    operation = operation(n)

root = nodes.pop()
root.calc()
print("Sum of metadata: {}".format(root.sum_metadata))
print("Root value: {}".format(root.value))
