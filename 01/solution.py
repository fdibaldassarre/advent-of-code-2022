import collections
import heapq


class Solver:
    def __init__(self):
        self.data = None

    def parse(self, input_file):
        self.data = list()
        self.data.append(list())
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip()
                if len(line) == 0:
                    self.data.append(list())
                    continue
                self.data[-1].append(int(line))

    def solve1(self):
        top_calories = 0
        for elf_pack in self.data:
            top_calories = max(top_calories, sum(elf_pack))
        return top_calories

    def solve2(self):
        top_calories = list()
        heapq.heapify(top_calories)
        for elf_pack in self.data:
            heapq.heappush(top_calories, sum(elf_pack))
            if len(top_calories) > 3:
                heapq.heappop(top_calories)
        return sum(top_calories)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
