#!/usr/bin/env python3


class LinkedRing:
    class Point:
        def __init__(self, value):
            self.value = value
            self.next = None
            self.prev = None

        def print(self):
            print(self.prev.value, "<--", self.value, "-->", self.next.value)

    def __init__(self, values):
        prev = None
        self.first = None
        self.zero = None
        self.length = len(values)
        for value in values:
            point = LinkedRing.Point(value)
            if value == 0:
                self.zero = point
            point.prev = prev
            if prev is not None:
                prev.next = point
            if self.first is None:
                self.first = point
            prev = point
        self.first.prev = point
        point.next = self.first

    def getNodes(self):
        nodes = list()
        nodes.append(self.first)
        current = self.first.next
        while current != self.first:
            nodes.append(current)
            current = current.next
        return nodes

    def to_list(self):
        result = list()
        for node in self.getNodes():
            result.append(node.value)
        return result

    def print(self):
        self.first.print()
        current = self.first.next
        while current != self.first:
            current.print()
            current = current.next

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        node.next = None
        node.prev = None

    def _insert_after(self, node, target):
        target_next = target.next
        # target -> node -> target_next

        target.next = node
        node.prev = target

        node.next = target_next
        target_next.prev = node

    def shift(self, node):
        value = node.value
        n_shifts = abs(value) % (self.length - 1)
        if n_shifts == 0:
            return
        if value > 0:
            current = node.next
        else:
            current = node.prev

        self._unlink(node)

        for i in range(1, n_shifts):
            current = current.next if value > 0 else current.prev
        if value < 0:
            current = current.prev

        # Insert after node
        self._insert_after(node, current)


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, input_file):
        self.data = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip()
                self.data.append(int(line))

    def run(self, values, n_mixes):
        ring = LinkedRing(values)
        nodes = ring.getNodes()
        for _ in range(n_mixes):
            for node in nodes:
                ring.shift(node)
        zero = ring.zero

        current = zero
        result = 0
        for i in range(3000):
            current = current.next
            if i + 1 == 1000 or i + 1 == 2000 or i + 1 == 3000:
                result += current.value
        return result

    def solve1(self):
        return self.run(self.data, 1)

    def solve2(self):
        values = [val * 811589153 for val in self.data]
        return self.run(values, 10)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
