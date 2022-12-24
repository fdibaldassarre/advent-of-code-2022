#!/usr/bin/env python3


DIRECTIONS = [
    ((0, -1), (-1, -1), (0, -1), (1, -1)),
    ((0, 1), (-1, 1), (0, 1), (1, 1)),
    ((-1, 0), (-1, -1), (-1, 0), (-1, 1)),
    ((1, 0), (1, -1), (1, 0), (1, 1))
]

def iterNeighbours(x, y):
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1


def vectorSum(a, b):
    res = [0] * len(a)
    for i in range(len(a)):
        res[i] = a[i] + b[i]
    return tuple(res)


def iterDirections(x, y, iter_number):
    for i in range(4):
        direction = DIRECTIONS[(iter_number + i) % 4]
        yield tuple(map(lambda el: vectorSum((x, y), el), direction))


class Solver:

    def __init__(self):
        self.elfs = None

    def parse(self, input_file):
        self.elfs = set()
        with open(input_file, "r") as hand:
            for y, line in enumerate(hand):
                line = line.strip()
                for x, ch in enumerate(line):
                    if ch == "#":
                        self.elfs.add((x, y))

    def getProposedMove(self, elf, positions, iter_number):
        x, y = elf
        moves = False
        for nx, ny in iterNeighbours(x, y):
            if (nx, ny) in positions:
                moves = True
                break
        if not moves:
            return None
        for candidate, check1, check2, check3 in iterDirections(x, y, iter_number):
            if check1 in positions or check2 in positions or check3 in positions:
                continue
            return candidate

    def getSquareSize(self, positions):
        min_x, max_x = None, 0
        min_y, max_y = None, 0
        for x, y in positions:
            if min_x is None:
                min_x = x
            if min_y is None:
                min_y = y
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return (min_x, min_y), (max_x, max_y)

    def printPositions(self, positions):
        (min_x, min_y), (max_x, max_y) = self.getSquareSize(positions)
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        result = [None] * height
        for y in range(height):
            row = ["."] * width
            for x in range(width):
                px = x + min_x
                py = y + min_y
                if (px, py) in positions:
                    row[x] = "#"
            result[y] = "".join(row)
        table = "\n".join(result)
        print(table)

    def iterOnce(self, current_positions, iter_number):
        proposed_moves = dict()
        new_positions = set()
        for elf in current_positions:
            position = self.getProposedMove(elf, current_positions, iter_number)
            if position is None:  # 861 is too low
                new_positions.add(elf)
                continue
            if position not in proposed_moves:
                proposed_moves[position] = set()
            proposed_moves[position].add(elf)
        iter_number += 1
        if len(proposed_moves) == 0:
            return False, current_positions
        for new_position, current_elfs in proposed_moves.items():
            if len(current_elfs) == 1:
                new_positions.add(new_position)
            else:
                for elf in current_elfs:
                    new_positions.add(elf)
        return True, new_positions

    def solve1(self):
        current_positions = self.elfs.copy()
        for iter_number in range(10):
            _, current_positions = self.iterOnce(current_positions, iter_number)
        (min_x, min_y), (max_x, max_y) = self.getSquareSize(current_positions)
        return (max_x - min_x + 1) * (max_y - min_y + 1) - len(current_positions)

    def solve2(self):
        current_positions = self.elfs.copy()
        iter_number = 0
        elfs_move = True
        while elfs_move:
            elfs_move, current_positions = self.iterOnce(current_positions, iter_number)
            iter_number += 1
        return iter_number


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
