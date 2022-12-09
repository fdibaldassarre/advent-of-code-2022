#!/usr/bin/env python3


MOVE_TO_DELTA = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

class Solver:

    def __init__(self):
        self.moves = None

    def parse(self, input_file):
        self.moves = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip().split(" ")
                self.moves.append((line[0], int(line[1])))

    def moveHead(self, point, move):
        delta = MOVE_TO_DELTA[move]
        return point[0] + delta[0], point[1] + delta[1]

    def getTailMotionOnAxis(self, direction):
        if direction == 0:
            return 0
        return 1 if direction > 0 else -1

    def moveTail(self, point_tail, point_head):
        delta_x = point_head[0] - point_tail[0]
        delta_y = point_head[1] - point_tail[1]
        if max(abs(delta_x), abs(delta_y)) <= 1:
            # Adiacent, do not move
            return point_tail
        dx = self.getTailMotionOnAxis(delta_x)
        dy = self.getTailMotionOnAxis(delta_y)
        return point_tail[0] + dx, point_tail[1] + dy

    def solve1(self):
        head = (0, 0)
        tail = (0, 0)
        visited = set()
        visited.add(tail)
        for move, spaces in self.moves:
            for _ in range(spaces):
                head = self.moveHead(head, move)
                tail = self.moveTail(tail, head)
                visited.add(tail)
        return len(visited)

    def solve2(self):
        head = (0, 0)
        nodes = [(0, 0) for _ in range(9)]
        visited = set()
        visited.add(nodes[-1])
        for move, spaces in self.moves:
            for _ in range(spaces):
                head = self.moveHead(head, move)
                prev = head
                for i in range(9):
                    nodes[i] = self.moveTail(nodes[i], prev)
                    prev = nodes[i]
                visited.add(nodes[-1])
        return len(visited)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
