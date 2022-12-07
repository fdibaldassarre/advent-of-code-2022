#!/usr/bin/env python3
import collections


class TreeNode:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.files = dict()
        self.children = dict()
        self.size = 0

    def addChildren(self, name):
        if name not in self.children:
            self.children[name] = TreeNode(name, self)
        return self.children[name]

    def addFile(self, name, size):
        if name not in self.files:
            self.files[name] = size
            self.updateSize(size)

    def updateSize(self, delta):
        self.size += delta
        if self.parent is not None:
            self.parent.updateSize(delta)

class Solver:

    def __init__(self):
        self.data = None
        self.root = None

    def parse(self, input_file):
        self.data = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip()
                self.data.append(line)
        self.populate()

    def populate(self):
        self.root = TreeNode("/")
        current = self.root
        i = 0
        while i < len(self.data):
            line = self.data[i]
            i += 1
            command = line[2:]
            if command == "ls":
                # ls
                while i < len(self.data) and not self.data[i].startswith("$"):
                    element = self.data[i]
                    i += 1
                    if element.startswith("dir"):
                        folder_name = element.split(" ", maxsplit=1)[1]
                        current.addChildren(folder_name)
                    else:
                        size_str, name = element.split(" ", maxsplit=1)
                        current.addFile(name, int(size_str))
            else:
                # cd
                folder = command.split(" ")[1]
                if folder == "/":
                    current = self.root
                elif folder == "..":
                    current = current.parent
                else:
                    current = current.children[folder]

    def iterFolders(self):
        border = collections.deque()
        border.append(self.root)
        while len(border) > 0:
            current = border.pop()
            yield current
            for child in current.children.values():
                border.append(child)

    def solve1(self):
        result = 0
        for current in self.iterFolders():
            if current.size < 100000:
                result += current.size
        return result

    def solve2(self):
        target = 30000000 - (70000000 - self.root.size)
        result = self.root.size
        for current in self.iterFolders():
            if result > current.size >= target:
                result = current.size
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
