#!/usr/bin/env python3
import re
import collections
MOVE_RE = re.compile("move (\d*) from (\d*) to (\d*)")

class Solver:

    def __init__(self):
        self.moves = None
        self.stacks = None

    def parse_crate_line(self, line):
        crates = list()
        if line.endswith("\n"):
            line = line[:-1]
            #print("'" + line + "'")
        #while i < len(line):
        for i in range(0, len(line), 4):
            #print("'" + line[i:i+3] + "'")
            if line[i] == " ":
                crates.append(None)
            else:
                crates.append(line[i+1])
            #i += 4
        return crates

    def parse(self, input_file):
        crates = list()
        self.moves = list()
        parse_moves = False
        with open(input_file, "r") as hand:
            for line in hand:
                line_strp = line.strip()
                if len(line_strp) == 0:
                    parse_moves = True
                    continue
                if parse_moves:
                    res = MOVE_RE.match(line_strp)
                    self.moves.append(tuple(map(int, res.groups())))
                else:
                    crates.append(self.parse_crate_line(line))
        n_stacks = len(crates.pop())
        self.stacks = []
        for i in range(n_stacks):
            stack = collections.deque()
            for j in range(len(crates), 0, -1):
                if crates[j-1][i] is None:
                    break
                stack.append(crates[j-1][i])
            self.stacks.append(stack)

    def get_stacks(self):
        stacks = list()
        for stack in self.stacks:
            stacks.append(stack.copy())
        return stacks

    def apply_move(self, move, current):
        n_el, source, target = move
        for i in range(n_el):
            current[target-1].append(current[source-1].pop())

    def apply_move9001(self, move, current):
        n_el, source, target = move
        elements = collections.deque()
        for i in range(n_el):
            elements.appendleft(current[source-1].pop())
        for el in elements:
            current[target-1].append(el)

    def solve(self, mover):
        current = self.get_stacks()
        for move in self.moves:
            mover(move, current)
        return "".join(map(lambda stack: stack.pop(), current))

    def solve1(self):
        return self.solve(self.apply_move)

    def solve2(self):
        return self.solve(self.apply_move9001)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %s" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %s" % solution2)
