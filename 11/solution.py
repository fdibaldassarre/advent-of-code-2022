#!/usr/bin/env python3
import collections


def getSubstring(hand, prefix):
    line = hand.readline().strip()
    if not line.startswith(prefix):
        raise Exception("Invalid " + line + ": Expected " + prefix)
    return line[len(prefix):]


class Monkey:
    def __init__(self):
        self.items = list()
        self.update_op = None
        self.test_condition = None
        self.target_if_true = None
        self.target_if_false = None

    def setItems(self, item):
        self.items.append(item)

    def setUpdateOperation(self, op_str):
        self.update_op = eval("lambda old: " + op_str)

    def setTestCondition(self, test_cond):
        self.test_condition = test_cond

    def setTargets(self, target_if_true, target_if_false):
        self.target_if_true = target_if_true
        self.target_if_false = target_if_false


class MonkeyInstance:
    def __init__(self, monkey):
        self._monkey = monkey
        self.test_condition = self._monkey.test_condition
        self._items = collections.deque(monkey.items)
        self.inspected_items = 0

    def iterItems(self, reduce_stress=False):
        while len(self._items) > 0:
            self.inspected_items += 1
            current = self._items.popleft()
            item_lvl = self._monkey.update_op(current)
            if reduce_stress:
                item_lvl = item_lvl // 3
            if item_lvl % self._monkey.test_condition == 0:
                yield item_lvl, self._monkey.target_if_true
            else:
                yield item_lvl, self._monkey.target_if_false

    def giveItem(self, item):
        self._items.append(item)


class Solver:

    def __init__(self):
        self.monkeys = None

    def parse(self, input_file):
        self.monkeys = list()
        with open(input_file, "r") as hand:
            line = ""
            while line is not None:
                new_monkey = Monkey()
                line = hand.readline().strip()  # Monkey :
                if line == "":
                    break
                starting_items = getSubstring(hand, "Starting items: ").split(", ")
                for item in starting_items:
                    new_monkey.setItems(int(item))
                operation = getSubstring(hand, "Operation: new = ")
                new_monkey.setUpdateOperation(operation)
                test_str = getSubstring(hand, "Test: divisible by ")
                new_monkey.setTestCondition(int(test_str))
                target_if_true = getSubstring(hand, "If true: throw to monkey ")
                target_if_false = getSubstring(hand, "If false: throw to monkey ")
                new_monkey.setTargets(int(target_if_true), int(target_if_false))
                self.monkeys.append(new_monkey)
                line = hand.readline()   # Empty line

    def run(self, rounds=20):
        reduce_stress = True if rounds == 20 else False
        current = [MonkeyInstance(monkey) for monkey in self.monkeys]
        test_condition_common = 1
        for monkey in current:
            test_condition_common *= monkey.test_condition
        for _ in range(rounds):
            for monkey in current:
                for item, target in monkey.iterItems(reduce_stress=reduce_stress):
                    item = item % test_condition_common
                    current[target].giveItem(item)
        most_inspected = sorted(current, key=lambda el: el.inspected_items, reverse=True)[:2]
        return most_inspected[0].inspected_items * most_inspected[1].inspected_items

    def solve1(self):
        return self.run(20)

    def solve2(self):
        return self.run(10000)


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
