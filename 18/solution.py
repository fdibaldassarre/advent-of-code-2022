#!/usr/bin/env python3


def iterSides(x, y, z):
    yield x - 1, y, z
    yield x + 1, y, z
    yield x, y - 1, z
    yield x, y + 1, z
    yield x, y, z - 1
    yield x, y, z + 1


class Explorer:

    def __init__(self, cubes):
        self.cubes = cubes
        self.external_zone = None
        self.max_x = None
        self.max_y = None
        self.max_z = None

    def init(self):
        max_x, max_y, max_z = 0, 0, 0
        for cube in self.cubes:
            x, y, z = cube
            max_x, max_y, max_z = max(x, max_x), max(y, max_y), max(z, max_z)
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        self.external_zone = self.exploreExternal()

    def exploreExternal(self):
        border = set()
        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                border.add((x, y, self.max_z + 1))
                border.add((x, y, -1))
            for z in range(self.max_z + 1):
                border.add((x, self.max_y + 1, z))
                border.add((x, -1, z))
        for y in range(self.max_y + 1):
            for z in range(self.max_z + 1):
                border.add((self.max_x + 1, y, z))
                border.add((-1, y, z))
        return self._explore(border)

    def explore(self, x, y, z):
        border = {(x, y, z)}
        return self._explore(border)

    def _explore(self, border):
        component = set(el for el in border)
        while len(border) > 0:
            x, y, z = border.pop()
            for dx, dy, dz in iterSides(x, y, z):
                if 0 <= dx <= self.max_x and 0 <= dy <= self.max_y and 0 <= dz <= self.max_z:
                    point = (dx, dy, dz)
                    if point in self.cubes or point in component:
                        continue
                    border.add(point)
                    component.add(point)
        return component


class Solver:

    def __init__(self):
        self.cubes = None

    def parse(self, input_file):
        self.cubes = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip().split(",")
                self.cubes.append(tuple(map(int, line)))

    def getSurface(self, cubes):
        grid = set()
        surface = 0
        for cube in cubes:
            x, y, z = cube
            surface += 6
            for side in iterSides(x, y, z):
                if side in grid:
                    surface -= 2
            grid.add(cube)
        return surface

    def solve1(self):
        return self.getSurface(self.cubes)

    def solve2(self):
        occupied = set(self.cubes)
        explorer = Explorer(occupied)
        explorer.init()
        surface = self.getSurface(occupied)
        explored = explorer.external_zone
        for x in range(explorer.max_x):
            for y in range(explorer.max_y):
                for z in range(explorer.max_z):
                    if (x, y, z) in occupied or (x, y, z) in explored:
                        continue
                    connected = explorer.explore(x, y, z)
                    surf_connected = self.getSurface(connected)
                    surface -= surf_connected
                    explored.update(connected)
        return surface


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
