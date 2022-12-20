#!/usr/bin/env python3


class Rock:

    def __init__(self, space, points):
        self.space = space
        self.points = points
        self.start = 2
        self.height = space.getMaxHeight() + 3

    def move(self, move):
        if move == "<":
            self.moveLeft()
        else:
            self.moveRight()

    def getSpaces(self):
        for dx, dy in self.points:
            yield self.start + dx, self.height + dy

    def moveRight(self):
        can_move = True
        for x, y in self.getSpaces():
            if self.space.isOccupied(x + 1, y):
                can_move = False
                break
        if can_move:
            self.start += 1

    def moveLeft(self):
        can_move = True
        for x, y in self.getSpaces():
            if self.space.isOccupied(x - 1, y):
                can_move = False
                break
        if can_move:
            self.start -= 1

    def moveDown(self):
        can_move = True
        for x, y in self.getSpaces():
            if self.space.isOccupied(x, y - 1):
                can_move = False
                break
        if can_move:
            self.height -= 1
        return can_move


class BarRock(Rock):
    name = "BarRock"

    def __init__(self, space):
        super().__init__(space, [(0, 0), (1, 0), (2, 0), (3, 0)])


class CrossRock(Rock):
    name = "CrossRock"

    def __init__(self, space):
        super().__init__(space, [(1, 0), (0, 1), (1, 1), (1, 2), (2, 1)])


class ReverseLRock(Rock):
    name = "ReverseLRock"

    def __init__(self, space):
        super().__init__(space, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])


class LongRock(Rock):
    name = "LongRock"

    def __init__(self, space):
        super().__init__(space, [(0, 0), (0, 1), (0, 2), (0, 3)])


class SquareRock(Rock):
    name = "SquareRock"

    def __init__(self, space):
        super().__init__(space, [(0, 0), (0, 1), (1, 0), (1, 1)])


class Space:

    def __init__(self):
        self.board = []
        self.levels = []

    def isOccupied(self, x, y):
        if y == -1:
            return True
        if x < 0 or x > 6:
            return True
        if y >= len(self.board):
            return False
        return self.board[y][x]

    def add(self, x, y):
        while y >= len(self.board):
            self.board.append([False]*7)
            self.levels.append(0)
        self.board[y][x] = True
        self.levels[y] = 0
        for i, el in enumerate(self.board[y]):
            if el:
                self.levels[y] += 2**i

    def getLevel(self, y):
        if y >= len(self.levels):
            return 0
        return self.levels[y]

    def getMaxHeight(self):
        return len(self.board)

    def print(self):
        res = ""
        for i in range(len(self.board), 0, -1):
            line = self.board[i - 1]
            res = res + "\n" + "".join(map(lambda el: "#" if el else " ", line))
        print(res)


class Board:

    def __init__(self):
        self.space = Space()
        self.last_moves = list()

    def iterRocks(self):
        while True:
            yield BarRock(self.space)
            yield CrossRock(self.space)
            yield ReverseLRock(self.space)
            yield LongRock(self.space)
            yield SquareRock(self.space)

    def addTile(self, x, y, rock, move_id, fallen_rocks):
        self.space.add(x, y)
        while len(self.last_moves) <= y:
            self.last_moves.append((None, None))
        self.last_moves[y] = (rock.name, move_id, fallen_rocks)

    def findPrevious(self, rock, move_id):
        expected_level = self.space.getLevel(rock.height)
        for y in range(rock.height - 1, 0, -1):
            old_lvl = self.space.getLevel(y)
            old_rock, old_move, fallen_rocks = self.last_moves[y]
            if old_lvl == expected_level and old_rock == rock.name and old_move == move_id:
                return y, fallen_rocks
        return -1, -1


class Solver:

    def __init__(self):
        self.data = None

    def parse(self, input_file):
        self.data = list()
        with open(input_file, "r") as hand:
            for line in hand:
                for ch in line:
                    self.data.append(ch)

    def iterMoves(self):
        while True:
            for i, el in enumerate(self.data):
                yield i, el

    def simulate(self, iterations):
        board = Board()
        rocks = board.iterRocks()
        moves = self.iterMoves()
        fallen_rocks = 0
        delta_size = None
        while fallen_rocks < iterations:
            rock = next(rocks)
            first_move, move = next(moves)
            rock.move(move)
            while rock.moveDown():
                _, move = next(moves)
                rock.move(move)
            fallen_rocks += 1
            for x, y in rock.getSpaces():
                board.addTile(x, y, rock, first_move, fallen_rocks)
            prev_lvl, prev_fallen = board.findPrevious(rock, first_move)
            if delta_size is None and prev_lvl > -1:
                repeat_size = rock.height - prev_lvl
                repeat_n_rocks = fallen_rocks - prev_fallen
                repeats = (iterations - fallen_rocks) // repeat_n_rocks
                delta_size = repeats * repeat_size
                fallen_rocks += repeats * repeat_n_rocks
        return delta_size + board.space.getMaxHeight()

    def solve1(self):
        return self.simulate(2022)

    def solve2(self):
        return self.simulate(1000000000000)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
