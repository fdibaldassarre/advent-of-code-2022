#!/usr/bin/env python3
import sys


def get_lzero_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_intersection_consecutive(interval_a, interval_b):
    size = interval_a[1] - interval_b[0] + 1
    return max(size, 0)


class BeaconCoverage:

    def __init__(self, center, size):
        self.center = center
        self.size = size

    def intersect(self, row):
        d = self.size - abs(row - self.center[1])
        return (self.center[0] - d, self.center[0] + d) if d >= 0 else None


class Solver:

    def __init__(self):
        self.beacons = None
        self.sensors = None
        self.coverage = None
        self.max_coord = -1

    def parse(self, input_file):
        self.beacons = list()
        self.sensors = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip().split(": ")
                beacon_pos = line[0][len("Sensor at "):].split(", ")
                sensor_pos = line[1][len("closest beacon is at "):].split(", ")
                beacon = tuple(map(lambda el: int(el[2:]), beacon_pos))
                sensor = tuple(map(lambda el: int(el[2:]), sensor_pos))
                self.beacons.append(beacon)
                self.sensors.append(sensor)
        self._computeCoverage()

    def _computeCoverage(self):
        self.coverage = [None] * len(self.beacons)
        for i, (beacon, sensor) in enumerate(zip(self.beacons, self.sensors)):
            self.coverage[i] = BeaconCoverage(beacon, get_lzero_distance(beacon, sensor))

    def computeIntersectionsWithRow(self, row):
        intersections = list()
        for coverage in self.coverage:
            intersection = coverage.intersect(row)
            if intersection is not None:
                intersections.append(intersection)
        intersections.sort(key=lambda el: el[0])
        return intersections

    def solve1(self):
        row = 2000000
        empty_beacons = self.computeIntersectionsWithRow(row)
        tot_size = 0
        max_x = None
        for i, interval in enumerate(empty_beacons):
            max_x = interval[0] if max_x is None else max(max_x, interval[0])
            if max_x is None:
                start_interval = interval[0]
            else:
                start_interval = max(interval[0], max_x+1)
            size = interval[1] - start_interval + 1
            if size <= 0:
                continue
            max_x = interval[1]
            tot_size += size
        return tot_size

    def _scanRow(self, row):
        all_intersect = self.computeIntersectionsWithRow(row)
        max_x = -1
        found = None
        for interval in all_intersect:
            if interval[0] > self.max_coord:
                break
            if max_x < interval[0] - 1:
                found = interval[0] - 1
                break
            max_x = max(max_x, interval[1])
        return found

    def solve2(self):
        self.max_coord = 4000000
        result = -1
        for y in range(self.max_coord):
            sys.stdout.write("\rScanned %.2f%% of the space" % ((1.0 * y / self.max_coord) * 100))
            x = self._scanRow(y)
            if x is not None:
                sys.stdout.write("\n")
                result = 4000000 * x + y
                break
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
