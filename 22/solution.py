#!/usr/bin/env python3


TURN_LEFT = "L"
TURN_RIGHT = "R"

TILE_WALL = "#"

FACE_UP = (0, -1)
FACE_DOWN = (0, 1)
FACE_RIGHT = (1, 0)
FACE_LEFT = (-1, 0)

ALL_2D_DIRECTIONS = [FACE_UP, FACE_RIGHT, FACE_UP, FACE_LEFT]

FACE_1 = (0, 0, 1)
FACE_2 = (0, 1, 0)
FACE_3 = (1, 0, 0)
FACE_4 = (-1, 0, 0)
FACE_5 = (0, -1, 0)
FACE_6 = (0, 0, -1)


def facingToScore(facing):
    if facing == FACE_RIGHT:
        return 0
    elif facing == FACE_DOWN:
        return 1
    elif facing == FACE_LEFT:
        return 2
    elif facing == FACE_UP:
        return 3
    else:
        raise Exception("Invalid facing" + str(facing))

def getIcon(facing):
    if facing == FACE_RIGHT:
        return ">"
    elif facing == FACE_DOWN:
        return "v"
    elif facing == FACE_LEFT:
        return "<"
    elif facing == FACE_UP:
        return "^"
    else:
        raise Exception("Invalid facing" + str(facing))


def scalarProduct(a, v):
    return tuple(map(lambda el: a * el, v))

def vectorSum(*vectors):
    result = [0] * len(vectors[0])
    for i in range(len(result)):
        for vector in vectors:
            result[i] += vector[i]
    return tuple(result)


class Space:
    def turnRight(self):
        raise Exception("Not implemented")

    def turnLeft(self):
        raise Exception("Not implemented")

    def move(self, steps):
        raise Exception("Not implemented")

    def getPosition(self):
        raise Exception("Not implemented")

    def getAbsolutePosition(self):
        raise Exception("Not implemented")

    def getDirection(self):
        raise Exception("Not implemented")


def convert_rows_to_string(rows, point, icon):
    levels = list()
    for y, (delta, row) in enumerate(rows):
        new_level = list()
        for _ in range(delta):
            new_level.append(' ')
        for x, ch in enumerate(row):
            if (x, y) == point:
                new_level.append(icon)
            else:
                new_level.append(ch)
        levels.append("".join(new_level))
    return "\n".join(levels)


class Plane(Space):

    def __init__(self, rows):
        self.rows = rows
        self.position = (0, 0)
        self.direction = (1, 0)

    def turnRight(self):
        self.direction = -1 * self.direction[1], self.direction[0]

    def turnLeft(self):
        self.direction = self.direction[1], -1 * self.direction[0]

    def move(self, steps):
        dx, dy = self.direction
        if dx == 0:
            for _ in range(steps):
                if not self._moveVertically(dy):
                    break
        else:
            for _ in range(steps):
                if not self._moveHorizontally(dx):
                    break

    def _moveVertically(self, dy):
        """
        Move one tile in the given direction (1 or -1)
        vertically.
        :param dy:
        :return:
        """
        y = self.position[1]
        current_delta, _ = self.rows[y]
        x = self.position[0]
        for i in range(len(self.rows)):
            new_y = (y + (i+1) * dy) % len(self.rows)
            new_delta, new_row = self.rows[new_y]
            new_x = x + current_delta - new_delta
            if 0 <= new_x < len(new_row):
                break
        if new_row[new_x] == TILE_WALL:
            return False
        else:
            self.position = (new_x, new_y)
            return True

    def _moveHorizontally(self, dx):
        """
        Move one tile in the given direction (1 or -1)
        vertically.
        :param dx:
        :return:
        """
        x, y = self.position
        _, row = self.rows[y]
        new_x = (x + dx) % len(row)
        if row[new_x] == TILE_WALL:
            return False
        else:
            self.position = (new_x, y)
            return True

    def getDirection(self):
        return self.direction

    def getPosition(self):
        return self.position

    def getAbsolutePosition(self):
        x, y = self.position
        delta, _ = self.rows[y]
        return x + delta, y

    def __str__(self):
        icon = getIcon(self.direction)
        return convert_rows_to_string(self.rows, self.position, icon)


class Cube(Space):
    def __init__(self, rows, cube, flatten):
        self.rows = rows
        self.cube = cube
        self.flatten = flatten
        self.position = (0, 0, 0)
        self.vector = FACE_1
        self.direction = (1, 0, 0)
        self.right = (0, 1, 0)

    def move(self, steps):
        for step in range(steps):
            if not self._moveOne():
                break

    def turnRight(self):
        self.direction, self.right = self.right, scalarProduct(-1, self.direction)

    def turnLeft(self):
        self.direction, self.right = scalarProduct(-1, self.right), self.direction

    def _moveOne(self):
        new_position = vectorSum(self.position, self.direction)
        new_direction = self.direction
        new_vector = self.vector
        if (new_position, new_vector) not in self.cube:
            # Rotate
            new_vector, new_direction = self.direction, scalarProduct(-1, self.vector)
            new_position = self.position
        if self.cube[(new_position, new_vector)] == TILE_WALL:
            return False
        else:
            self.position = new_position
            self.direction = new_direction
            self.vector = new_vector
            return True

    def getPosition(self):
        return self.flatten[(self.position, self.vector)]

    def getAbsolutePosition(self):
        x, y = self.getPosition()
        delta, _ = self.rows[y]
        return x + delta, y

    def getDirection(self):
        front = vectorSum(self.position, self.direction)
        if (front, self.vector) in self.cube:
            start = self.flatten[(self.position, self.vector)]
            end = self.flatten[(front, self.vector)]
        else:
            back = vectorSum(self.position, scalarProduct(-1, self.direction))
            start = self.flatten[(back, self.vector)]
            end = self.flatten[(self.position, self.vector)]
        return vectorSum(end, scalarProduct(-1, start))

    def __str__(self):
        icon = getIcon(self.getDirection())
        position2d = self.getPosition()
        return convert_rows_to_string(self.rows, position2d, icon)


class CubeBuilder:
    def __init__(self, rows):
        self.rows = rows
        self.size = 50

    def rotateRight(self, vector):
        x, y, z = vector
        return z, y, -x

    def rotateLeft(self, vector):
        x, y, z = vector
        return -z, y, x

    def rotateUp(self, vector):
        x, y, z = vector
        return x, -z, y

    def rotateDown(self, vector):
        x, y, z = vector
        return x, z, -y

    def build(self):
        border = set()
        border.add(((0, 0), (0, 0, 0), (1, 0, 0), (0, 1, 0), FACE_1))

        cube = dict()
        flatten_map = dict()  # map of point on cube to 2d-point

        faces = dict()
        while len(border) > 0:
            (x, y), start, vx, vy, face = border.pop()
            faces[face] = set()
            delta, base_row = self.rows[y]
            for dy in range(self.size):
                _, row = self.rows[y + dy]
                for dx in range(self.size):
                    faces[face].add(row[x])
                    point = vectorSum(start, scalarProduct(dx, vx), scalarProduct(dy, vy))
                    cube[(point, face)] = row[x + dx]
                    flatten_map[(point, face)] = (x + dx, y + dy)
            # Check on the right
            if x + self.size < len(base_row):
                new_x = x + self.size
                new_start = vectorSum(start, scalarProduct(self.size - 1, vx))
                # Rotate such that
                # rot(face) = vx
                new_vx = scalarProduct(-1, face)
                new_vy = vy
                new_face = vx
                if new_face not in faces:
                    border.add(((new_x, y), new_start, new_vx, new_vy, new_face))
            # Check on the left
            if x - self.size >= 0:
                new_x = x - self.size
                new_start = vectorSum(start, scalarProduct(-1 * (self.size - 1), face))
                # Rotate such that
                # rot(face) = -vx
                new_vx = face
                new_vy = vy
                new_face = scalarProduct(-1, vx)
                if new_face not in faces:
                    border.add(((new_x, y), new_start, new_vx, new_vy, new_face))
            # Check down
            new_y = y + self.size
            if new_y >= len(self.rows):
                continue
            new_delta, new_row = self.rows[new_y]
            new_x = x + delta - new_delta
            if 0 <= new_x < len(new_row):
                # Rotate such that
                # rotation(face) = vy
                new_start = vectorSum(start, scalarProduct(self.size - 1, vy))
                new_vx = vx
                new_vy = scalarProduct(-1, face)
                new_face = vy
                border.add(((new_x, new_y), new_start, new_vx, new_vy, new_face))

        return Cube(self.rows, cube, flatten_map)


class Solver:

    def __init__(self):
        self.rows = None
        self.instructions = None

    def parse(self, input_file):
        self.rows = list()
        self.instructions = list()
        parse_instructions = False
        with open(input_file, "r") as hand:
            for line_raw in hand:
                line = line_raw.strip()
                if line == "":
                    parse_instructions = True
                    continue
                if parse_instructions:
                    prev = 0
                    for i, ch in enumerate(line):
                        if ch == "L" or ch == "R":
                            self.instructions.append(int(line[prev:i]))
                            self.instructions.append(ch)
                            prev = i + 1
                    if prev < len(line):
                        self.instructions.append(int(line[prev:len(line)]))
                    assert line == "".join(map(str, self.instructions))
                else:
                    delta = 0
                    for ch in line_raw:
                        if ch == " ":
                            delta += 1
                        else:
                            break
                    self.rows.append((delta, line))

    def run(self, space):
        for instruction in self.instructions:
            if instruction == TURN_LEFT:
                space.turnLeft()
            elif instruction == TURN_RIGHT:
                space.turnRight()
            else:
                space.move(instruction)
        col, row = space.getAbsolutePosition()
        direction = space.getDirection()
        #print(col, row)
        #print(facingToScore(direction))
        return 1000 * (row + 1) + 4 * (col + 1) + facingToScore(direction)

    def solve1(self):
        plane = Plane(self.rows)
        return self.run(plane)

    def solve2(self):
        builder = CubeBuilder(self.rows)
        cube = builder.build()
        return self.run(cube)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
