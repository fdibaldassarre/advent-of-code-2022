#!/usr/bin/env python3
import collections


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, input_file):
        self.data = list()
        with open(input_file, "r") as hand:
            self.data = hand.readline().strip()

    def solve(self, target):
        current = collections.defaultdict(int)
        for i, ch in enumerate(self.data):
            if i < target:
                current[ch] += 1
            else:
                if max(current.values()) == 1:
                    break
                else:
                    prev = self.data[i-target]
                    current[prev] -= 1
                    if current[prev] == 0:
                        del current[prev]
                    current[ch] += 1
        return i

    def solve1(self):
        return self.solve(target=4)

    def solve2(self):
        return self.solve(target=14)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
