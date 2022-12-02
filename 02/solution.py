import collections
import heapq


SHAPE_TO_SCORE = {
    'R': 1, 'P': 2, 'S': 3
}

SHAPE_TO_VAL = {
    'R': 0, 'P': 1, 'S': 2
}

VAL_TO_SHAPE = ['R', 'P', 'S']


def check_winner(a, b):
    """
    Return 1 if is a draw, 2 if b wins, 0 if a wins
    """
    if a == b:
        return 1
    if SHAPE_TO_VAL[b] == (SHAPE_TO_VAL[a]+1) % 3:
        return 2  # b > a
    return 0


class Solver:

    CONVERTER = {
        'A': 'R', 'B': 'P', 'C': 'S',
        'X': 'R', 'Y': 'P', 'Z': 'S'
    }

    SCORE_CONVERTER = {
        'X': 0, 'Y': 1, 'Z': 2
    }

    def __init__(self):
        self.data = None

    def parse(self, input_file):
        self.data = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip().split(" ", maxsplit=2)
                self.data.append(line)

    def solve1(self):
        score = 0
        for moves in self.data:
            elf, me = list(map(lambda m: Solver.CONVERTER[m], moves))
            result = check_winner(elf, me)
            score += (3 * result + SHAPE_TO_SCORE[me])
        return score

    def solve2(self):
        score = 0
        for moves in self.data:
            elf, result = moves
            elf = Solver.CONVERTER[elf]
            if result == 'X':
                # lose
                me = VAL_TO_SHAPE[(SHAPE_TO_VAL[elf] - 1) % 3]
            elif result == 'Y':
                # draw
                me = elf
            else:
                # win
                me = VAL_TO_SHAPE[(SHAPE_TO_VAL[elf] + 1) % 3]
            score += (3 * Solver.SCORE_CONVERTER[result] + SHAPE_TO_SCORE[me])
        return score


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
