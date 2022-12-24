#!/usr/bin/env python3
import math
import heapq


MOVEMENTS = {
    ">": (1, 0),
    "v": (0, 1),
    "^": (0, -1),
    "<": (-1, 0)
}


class Valley:

    def __init__(self, width, height, blizzards):
        self.width = width
        self.height = height
        self.period = math.lcm(self.width, self.height)
        self.blizzards = blizzards

    def updateBlizzards(self):
        new_blizzards = dict()
        for (x, y), directions in self.blizzards.items():
            for direction in directions:
                dx, dy = MOVEMENTS[direction]
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                if (nx, ny) not in new_blizzards:
                    new_blizzards[(nx, ny)] = list()
                new_blizzards[(nx, ny)].append(direction)
        self.blizzards = new_blizzards

    def getFreeSpaces(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.blizzards:
                    yield x, y

    def getNeighbours(self, x, y):
        yield x, y
        if x > 0:
            yield x - 1, y
        if x < self.width - 1:
            yield x + 1, y
        if y > 0:
            yield x, y - 1
        if y < self.height - 1:
            yield x, y + 1

    def __str__(self):
        result = list()
        for y in range(self.height):
            row = ["."] * self.width
            for x in range(self.width):
                if (x, y) in self.blizzards:
                    row[x] = self.blizzards[(x, y)][0]
            result.append("".join(row))
        return "\n".join(result)


class ValleyStatus:

    def __init__(self, valley):
        self.valley = valley
        self.free_spaces_per_turn = [None] * self.valley.period

    def load(self):
        for i in range(self.valley.period):
            self.free_spaces_per_turn[i] = set()
            for x, y in self.valley.getFreeSpaces():
                self.free_spaces_per_turn[i].add((x, y))
            self.valley.updateBlizzards()

    def getFreePoints(self, turn):
        return self.free_spaces_per_turn[turn % self.valley.period]


class StatusQueue:

    def __init__(self, target):
        self.tx, self.ty = target
        self.queue = list()
        heapq.heapify(self.queue)

    def _estimate(self, x, y, turn):
        return turn + abs(self.tx - x) + abs(self.ty - y)

    def add(self, x, y, turn):
        estimate = self._estimate(x, y, turn)
        heapq.heappush(self.queue, (estimate, turn, x, y))

    def pop(self):
        estimate, turn, x, y = heapq.heappop(self.queue)
        return estimate, x, y, turn

    def isEmpty(self):
        return len(self.queue) == 0


class Solver:

    def __init__(self):
        self.width = -1
        self.height = -1
        self.blizzards = None
        self.start = None
        self.target = None
        self.valley = None
        self.valley_status = None

    def parse(self, input_file):
        self.blizzards = dict()
        with open(input_file, "r") as hand:
            self.height = 0
            for line in hand:
                line = line.strip()
                if line[2] == "#":
                    continue
                space = line[1:-1]
                for x, ch in enumerate(space):
                    if ch != ".":
                        self.blizzards[(x, self.height)] = [ch]
                self.height += 1
                self.width = len(line) - 2
        self.valley = Valley(self.width, self.height, self.blizzards)
        self.valley_status = ValleyStatus(self.valley)
        self.valley_status.load()

    def run(self, start, starting_turn, target):
        statuses = StatusQueue(target)
        for wait_time in range(self.valley.period):
            turn = starting_turn + wait_time
            free_points = self.valley_status.getFreePoints(turn)
            if start in free_points:
                statuses.add(*start, turn)
        best_result = -1
        explored = set()
        while not statuses.isEmpty():
            estimate, x, y, turn = statuses.pop()
            if (x, y, turn) in explored:
                continue
            if estimate >= best_result > -1:
                continue
            if (x, y) == target:
                best_result = turn
                continue
            free_points = self.valley_status.getFreePoints(turn + 1)
            for nx, ny in self.valley.getNeighbours(x, y):
                if (nx, ny) in free_points:
                    statuses.add(nx, ny, turn + 1)
            explored.add((x, y, turn))
        return best_result + 1

    def solve1(self):
        start = (0, 0)
        target = (self.valley.width - 1, self.valley.height - 1)
        starting_turn = 0
        return self.run(start, starting_turn, target)

    def solve2(self):
        start = (0, 0)
        target = (self.valley.width - 1, self.valley.height - 1)
        starting_turn = 0
        end_turn = self.run(start, starting_turn, target)
        end_turn2 = self.run(target, end_turn, start)
        return self.run(start, end_turn2, target)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
