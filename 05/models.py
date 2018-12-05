class UnitNode:
    def __init__(self, unit):
        self.prev = None
        self.next = None
        self.unit = unit

    def insert_self_after(self, node):
        if not node.next is None:
            self.next = node.next
            self.next.prev = self
        node.next = self
        self.prev = node
        return self

    def remove_self(self):
        prev = self.prev
        next = self.next
        if not prev is None:
            prev.next = next
        if not next is None:
            next.prev = prev
        self.prev = self.next = None
        return prev

    def get_length(self):
        n = 0
        node = self
        while not node is None:
            n += 1
            node = node.next
        return n

    def __iter__(self):
        return self.Iterator(self)

    class Iterator:
        def __init__(self, node):
            self.node = node

        def __next__(self):
            if self.node is None:
                raise StopIteration
            result = self.node
            self.node = self.node.next
            return result
