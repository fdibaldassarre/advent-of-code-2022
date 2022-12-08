#!/usr/bin/env python3


class Solver:

    def __init__(self):
        self.grid = None
        self.N = -1
        self.M = -1

    def parse(self, input_file):
        self.grid = list()
        with open(input_file, "r") as hand:
            for line in hand:
                self.grid.append(line.strip())
        self.N = len(self.grid)
        self.M = len(self.grid[0])

    def isCorner(self, point):
        return (point[0] == 0 or point[0] == self.N - 1) and \
               (point[1] == 0 or point[1] == self.M - 1)

    def rotate(self, point):
        return point[1], -1 * point[0]

    def lookInside(self, point, look):
        n_iter = self.N-1 if look[1] == 0 else self.M-1
        for i in range(1, n_iter):
            yield point[0] + i * look[0], point[1] + i * look[1]

    def getTree(self, point):
        return int(self.grid[point[0]][point[1]])

    def solve1(self):
        direction = [0, 1]
        look = [1, 0]
        current = (0, 1)
        visible = set()
        while current not in visible:
            visible.add(current)
            if self.isCorner(current):
                direction = self.rotate(direction)
                look = self.rotate(look)
            else:
                # Look
                max_tree_size = self.getTree(current)
                for point in self.lookInside(current, look):
                    tree_size = self.getTree(point)
                    if tree_size > max_tree_size:
                        visible.add(point)
                        max_tree_size = tree_size
            # Next
            current = (current[0] + direction[0], current[1] + direction[1])
        return len(visible)

    def lookAlong(self, point, look):
        n_iter = self.N if look[1] == 0 else self.M
        for i in range(1, n_iter):
            candidate_x = point[0] + i * look[0]
            candidate_y = point[1] + i * look[1]
            if 0 <= candidate_x < self.N and 0 <= candidate_y < self.M:
                yield candidate_x, candidate_y

    def getScore(self, point):
        look = [1, 0]
        score = 1
        top_tree = self.getTree(point)
        for i in range(4):
            visible = 0
            for target in self.lookAlong(point, look):
                current_tree = self.getTree(target)
                visible += 1
                if current_tree >= top_tree:
                    break
            look = self.rotate(look)
            score = score * visible
            if score == 0:
                break
        return score

    def solve2(self):
        best_score = 0
        for x in range(1, self.N - 1):
            for y in range(1, self.M - 1):
                best_score = max(best_score, self.getScore((x, y)))
        return best_score


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
