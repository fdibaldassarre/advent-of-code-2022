#!/usr/bin/env python3

OP_SUM = "+"
OP_SUB = "-"
OP_PRD = "*"
OP_DIV = "/"

VAR_ROOT = "root"
VAR_HUMN = "humn"


class Operation:
    def eval(self, closure):
        raise Exception("Not implemented")

    def invert(self, closure, expected):
        """
        Return the variable and value to add to the
        closure such that the operation returns
        the expected value
        :param closure:
        :param expected:
        :return:
        """
        raise Exception("Not implemented")


class Constant(Operation):
    def __init__(self, value):
        self.value = value

    def eval(self, closure):
        return self.value

    def invert(self, closure, expected):
        raise Exception("Not implemented")


class ArithmeticOperation(Operation):
    def __init__(self, operation, variable1, variable2):
        self.operation = operation
        self.variable1 = variable1
        self.variable2 = variable2
        if operation == OP_SUM:
            self.executor = lambda el1, el2: el1 + el2
        elif operation == OP_SUB:
            self.executor = lambda el1, el2: el1 - el2
        elif operation == OP_PRD:
            self.executor = lambda el1, el2: el1 * el2
        elif operation == OP_DIV:
            self.executor = lambda el1, el2: int(el1 / el2)
        else:
            raise Exception("Unknown operation " + operation)

    def eval(self, closure):
        val1 = closure[self.variable1]
        val2 = closure[self.variable2]
        return self.executor(val1, val2)

    def getFreeVariables(self):
        return self.variable1, self.variable2

    def invert(self, closure, expected):
        if self.operation == OP_SUM:
            # var1 + var2 = expected
            if self.variable1 in closure:
                # var2 = expected - variable1
                return self.variable2, expected - closure[self.variable1]
            else:
                return self.variable1, expected - closure[self.variable2]
        elif self.operation == OP_SUB:
            # var1 - var2 = expected
            if self.variable1 in closure:
                # var2 = -1 * (expected - variable1)
                return self.variable2, -1 * (expected - closure[self.variable1])
            else:
                # var1 = expected + var2
                return self.variable1, expected + closure[self.variable2]
        elif self.operation == OP_DIV:
            # var1 / var2 = expected
            if self.variable1 in closure:
                # var2 = var1 / expected
                return self.variable2, int(closure[self.variable1] / expected)
            else:
                # var1 = expected * var2
                return self.variable1, expected * closure[self.variable2]
        else:
            # var1 * var2 = expected
            if self.variable1 in closure:
                # var2 = expected / var1
                return self.variable2, int(expected / closure[self.variable1])
            else:
                # var1 = expected / var2
                return self.variable1, int(expected / closure[self.variable2])


class EqualityOperation(Operation):
    def __init__(self, variable1, variable2):
        self.variable1 = variable1
        self.variable2 = variable2

    def eval(self, closure):
        val1 = closure[self.variable1]
        val2 = closure[self.variable2]
        return val1 == val2

    def invert(self, closure, expected):
        if expected:
            if self.variable1 in closure:
                val1 = closure[self.variable1]
                return self.variable2, val1
            else:
                val2 = closure[self.variable2]
                return self.variable1, val2
        else:
            raise Exception("Not implemented")


class Solver:

    def __init__(self):
        self.monkey_to_op = None
        self.execution_levels = None
        self.human_deps = None

    def parse(self, input_file):
        self.monkey_to_op = dict()
        self.execution_levels = list()
        self.execution_levels.append([])
        pending = set()
        dependencies = dict()
        with open(input_file, "r") as hand:
            for line in hand:
                monkey, operation_raw = line.strip().split(": ", maxsplit=2)
                if " " in operation_raw:
                    operation = ArithmeticOperation(operation_raw[5], operation_raw[:4], operation_raw[-4:])
                    pending.add(monkey)
                    for var in operation.getFreeVariables():
                        if var not in dependencies:
                            dependencies[var] = list()
                        dependencies[var].append(monkey)
                else:
                    operation = Constant(int(operation_raw))
                    self.execution_levels[0].append(monkey)
                self.monkey_to_op[monkey] = operation
        # Variables dependent from the human
        self.human_deps = set()
        self.human_deps.add(VAR_HUMN)
        last_dep = VAR_HUMN
        while last_dep in dependencies:
            last_dep = dependencies[last_dep][0]
            self.human_deps.add(last_dep)
        while len(pending) > 0:
            prev_lvl = self.execution_levels[-1]
            new_level = list()
            for monkey in prev_lvl:
                for dep_monkey in dependencies[monkey]:
                    if dep_monkey not in pending:
                        continue
                    dep_op = self.monkey_to_op[dep_monkey]
                    can_be_computed = True
                    for var in dep_op.getFreeVariables():
                        if var in pending:
                            can_be_computed = False
                            break
                    if can_be_computed:
                        new_level.append(dep_monkey)
                        pending.remove(dep_monkey)
            self.execution_levels.append(new_level)

    def solve1(self):
        closure = dict()
        for lvl in self.execution_levels:
            for monkey in lvl:
                operation = self.monkey_to_op[monkey]
                closure[monkey] = operation.eval(closure)
        return closure[VAR_ROOT]

    def solve2(self):
        root_vars = self.monkey_to_op[VAR_ROOT].getFreeVariables()
        self.monkey_to_op[VAR_ROOT] = EqualityOperation(*root_vars)
        closure = dict()
        for lvl in self.execution_levels:
            for monkey in lvl:
                if monkey in self.human_deps:
                    continue
                operation = self.monkey_to_op[monkey]
                closure[monkey] = operation.eval(closure)
        current = VAR_ROOT
        expected_value = True
        while current != VAR_HUMN:
            op = self.monkey_to_op[current]
            current, expected_value = op.invert(closure, expected_value)
        return expected_value


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
