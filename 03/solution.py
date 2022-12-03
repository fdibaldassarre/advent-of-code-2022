

def get_priority(element):
    if element.isupper():
        return ord(element) - ord('A') + 27
    else:
        return ord(element) - ord('a') + 1

class Solver:

    def __init__(self):
        self.data = None

    def parse(self, input_file):
        self.data = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip()
                self.data.append(line)

    def solve1(self):
        tot_priorities = 0
        for rucksack in self.data:
            first_half = set(rucksack[:len(rucksack) // 2])
            second_half = set(rucksack[len(rucksack)//2:])
            common = first_half.intersection(second_half).pop()
            tot_priorities += get_priority(common)
        return tot_priorities

    def solve2(self):
        tot_priorities = 0
        for group in range(int(len(self.data)//3)):
            common_items = set(self.data[3 * group])
            common_items = common_items.intersection(self.data[3 * group + 1])
            common_items = common_items.intersection(self.data[3 * group + 2])
            common = common_items.pop()
            tot_priorities += get_priority(common)
        return tot_priorities


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
