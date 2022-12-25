#!/usr/bin/env python3

SNAFU_CH_TO_INT = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2
}


def toBaseFive(value):
    if value == 0:
        return [0]
    el = value % 5
    if el == 0:
        result = toBaseFive(value // 5)
        result.append(0)
    else:
        result = toBaseFive(value - el)
        result[-1] = el
    return result


def toSnafu(value):
    base_five = toBaseFive(value)
    base_five.reverse()
    rem = 0
    result = list()
    i = 0
    while i < len(base_five) or rem > 0:
        val = base_five[i] if i < len(base_five) else 0
        i += 1
        val = val + rem
        rem = val // 5
        val = val % 5
        if 0 <= val <= 2:
            result.append(str(val))
        elif val == 3:
            result.append("=")
            rem += 1
        else:
            result.append("-")
            rem += 1
    result.reverse()
    return "".join(result)


def fromSnafu(value):
    result = 0
    for ch in value:
        result = result * 5 + SNAFU_CH_TO_INT[ch]
    return result


class Solver:

    def __init__(self):
        self.values = None

    def parse(self, input_file):
        self.values = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip()
                self.values.append(line)

    def solve1(self):
        total = 0
        for value in self.values:
            total += fromSnafu(value)
        return toSnafu(total)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %s" % solution1)
