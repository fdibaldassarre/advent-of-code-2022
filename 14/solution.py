#!/usr/bin/env python3
import bisect


class ImpactChecker:

    def __init__(self):
        self.horizontal_lines = dict()
        self.vertical_lines = dict()
        self.floor_level = -1

    def addLine(self, point_a, point_b):
        if point_a[0] == point_b[0]:
            self._addVerticalLine(point_a, point_b)
        else:
            self._addHorizontalLine(point_a, point_b)

    def _addHorizontalLine(self, point_a, point_b):
        y = point_a[1]
        x_start = min(point_a[0], point_b[0])
        x_end = max(point_a[0], point_b[0])
        if y not in self.horizontal_lines:
            self.horizontal_lines[y] = list()
        self.horizontal_lines[y].append((x_start, x_end))

    def _addVerticalLine(self, point_a, point_b):
        x = point_a[0]
        y_start = min(point_a[1], point_b[1])
        y_end = max(point_a[1], point_b[1])
        if x not in self.vertical_lines:
            self.vertical_lines[x] = list()
        self.vertical_lines[x].append((y_start, y_end))

    def finalize(self):
        for lines in self.horizontal_lines.values():
            lines.sort(key=lambda el: el[0])
        for lines in self.vertical_lines.values():
            lines.sort(key=lambda el: el[0])

    def _checkHorizontalImpact(self, point):
        x, y = point
        if y not in self.horizontal_lines:
            return False
        horizontal_lines = self.horizontal_lines[y]
        idx = bisect.bisect_right(horizontal_lines, x, key=lambda el: el[0])
        candidate = horizontal_lines[idx-1]
        return candidate[0] <= x <= candidate[1]

    def _checkVerticalImpact(self, point):
        x, y = point
        if y == self.floor_level:
            # Hit the floor
            return True
        if x not in self.vertical_lines:
            return False
        vertical_lines = self.vertical_lines[x]
        idx = bisect.bisect_right(vertical_lines, y, key=lambda el: el[0])
        candidate = vertical_lines[idx-1]
        return candidate[0] <= y <= candidate[1]

    def checkImpact(self, point):
        return self._checkHorizontalImpact(point) or self._checkVerticalImpact(point)


class Solver:

    def __init__(self):
        self.max_y = -1
        self.grains = set()
        self._impact_checker = ImpactChecker()
        self._consider_floor = False

    def parse(self, input_file):
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip().split(" -> ")
                prev_point = None
                for point in line:
                    point_pair = tuple(map(int, point.split(",")))
                    if prev_point is not None:
                        self._impact_checker.addLine(prev_point, point_pair)
                    prev_point = point_pair
                    self.max_y = max(self.max_y, point_pair[1])
        self._impact_checker.finalize()

    def addFloor(self):
        self._consider_floor = True
        self._impact_checker.floor_level = self.max_y + 2

    def getNewPositions(self, point):
        yield point[0], point[1] + 1
        yield point[0] - 1, point[1] + 1
        yield point[0] + 1, point[1] + 1

    def isContained(self, point, start_line, end_line):
        min_start = min(start_line[0], end_line[0])
        max_start = max(start_line[0], end_line[0])
        min_end = min(start_line[1], end_line[1])
        max_end = max(start_line[1], end_line[1])
        return min_start <= point[0] <= max_start and \
            min_end <= point[1] <= max_end

    def isFree_old(self, point):
        if point in self.grains:
            return False
        for line in self.lines:
            for i in range(1, len(line)):
                if self.isContained(point, line[i-1], line[i]):
                    return False
        return True

    def isFree(self, point):
        if point in self.grains:
            return False
        return not self._impact_checker.checkImpact(point)

    def fallsForever(self, position):
        if self._consider_floor:
            return False
        return position[1] > self.max_y

    def dropSandGain(self):
        position = (500, 0)
        can_fall = True
        while can_fall:
            can_fall = False
            for new_position in self.getNewPositions(position):
                if self.isFree(new_position):
                    position = new_position
                    can_fall = True
                    break
            if can_fall and self.fallsForever(position):
                break
        return None if can_fall else position

    def solve(self):
        grain_falls_forever = False
        while not grain_falls_forever:
            pos = self.dropSandGain()
            if pos is None:
                grain_falls_forever = True
            else:
                self.grains.add(pos)
                if pos[1] == 0:
                    break
        return len(self.grains)

    def solve1(self):
        return self.solve()

    def solve2(self):
        self.addFloor()
        return self.solve()


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")

    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
