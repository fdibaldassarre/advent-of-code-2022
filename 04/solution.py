

def contains(interval1, interval2):
    """
    :param interval1:
    :param interval2:
    :return: true if interval1 is contained in interval2
    """
    return interval2[0] <= interval1[0] and interval1[1] <= interval2[1]


def overlap(interval1, interval2):
    return interval2[0] <= interval1[0] <= interval2[1] or \
            interval1[0] <= interval2[0] <= interval1[1]

class Solver:

    def __init__(self):
        self.data = None

    def parse(self, input_file):
        self.data = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip().split(",")
                interval1 = list(map(int, line[0].split("-")))
                interval2 = list(map(int, line[1].split("-")))
                self.data.append((interval1, interval2))

    def solve1(self):
        fully_contained = 0
        for interval1, interval2 in self.data:
            if contains(interval1, interval2) or contains(interval2, interval1):
                fully_contained += 1
        return fully_contained

    def solve2(self):
        overlapping = 0
        for interval1, interval2 in self.data:
            if overlap(interval1, interval2):
                overlapping += 1
        return overlapping


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
