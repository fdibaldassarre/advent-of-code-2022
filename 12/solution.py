#!/usr/bin/env python3
import heapq

class Solver:

    def __init__(self):
        self.heightmap = None
        self.N = None
        self.M = None
        self.start = None
        self.end = None
        self.startIsMarked = True

    def parse(self, input_file):
        self.heightmap = list()
        with open(input_file, "r") as hand:
            for x, line in enumerate(hand):
                line = line.strip()
                self.heightmap.append(line)
                s_idx = line.find('S')
                if s_idx > -1:
                    self.start = (x, s_idx)
                e_idx = line.find('E')
                if e_idx > -1:
                    self.end = (x, e_idx)
        self.N = len(self.heightmap)
        self.M = len(self.heightmap[0])

    def iterNeighbours(self, point):
        x, y = point
        if x > 0:
            yield x - 1, y
        if x < self.N - 1:
            yield x + 1, y
        if y > 0:
            yield x, y - 1
        if y < self.M - 1:
            yield x, y + 1

    def getHeight(self, point):
        x, y = point
        ch = self.heightmap[x][y]
        if ch == 'S':
            ch = 'a'
        elif ch == 'E':
            ch = 'z'
        return ord(ch) - ord('a')

    def isPossibleStartPoint(self, point):
        if self.startIsMarked:
            return point[0] == self.start[0] and point[1] == self.start[1]
        else:
            return self.getHeight(point) == 0

    def solve1(self):
        self.startIsMarked = True
        return self.solve()

    def solve2(self):
        self.startIsMarked = False
        return self.solve()

    def solve(self):
        explored = set()
        border = list()
        heapq.heapify(border)
        heapq.heappush(border, (0, self.end))
        explored.add(self.end)
        solution = -1
        while len(border) > 0 and solution == -1:
            current_steps, current_point = heapq.heappop(border)
            current_height = self.getHeight(current_point)
            for neighbour_point in self.iterNeighbours(current_point):
                neighbour_height = self.getHeight(neighbour_point)
                if neighbour_point in explored:
                    continue
                if neighbour_height >= current_height - 1:
                    if self.isPossibleStartPoint(neighbour_point):
                        solution = current_steps + 1
                        break
                    heapq.heappush(border, (current_steps + 1, neighbour_point))
                    explored.add(neighbour_point)
        return solution


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
