#!/usr/bin/env python3


class Solver:

    def __init__(self):
        self.instructions = None

    def parse(self, input_file):
        self.instructions = list()
        with open(input_file, "r") as hand:
            for line in hand:
                self.instructions.append(line.strip())

    def executeCycles(self):
        cycle = 1
        x = 1
        for instruction in self.instructions:
            yield cycle, x
            if instruction == "noop":
                cycle += 1
            else:
                _, qty = instruction.split(" ")
                qty = int(qty)
                yield cycle+1, x
                x += qty
                cycle += 2
        yield cycle, x

    def solve1(self):
        result = 0
        next_target = 20
        for cycle, x in self.executeCycles():
            if cycle == next_target:
                result += x * cycle
                if next_target < 220:
                    next_target += 40
        return result

    def printCrt(self, crt):
        res = list()
        for i in range(6):
            res.append("".join(crt[i * 40: (i+1)*40]).replace(".", " "))
        print("\n".join(res))

    def solve2(self):
        crt = ["."] * (40*6)
        for cycle, x in self.executeCycles():
            crt_pos = cycle-1
            hor_pos = crt_pos % 40
            if x - 1 <= hor_pos <= x + 1:
                crt[crt_pos] = "#"
        return crt


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2:")
    solver.printCrt(solution2)

