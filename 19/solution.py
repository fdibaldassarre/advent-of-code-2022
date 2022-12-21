#!/usr/bin/env python3
import re
import math
import heapq

RE_ORE_COST = re.compile(".* costs (\d*) ore")
RE_CLAY_COST = re.compile(".* costs (\d*) ore and (\d*) clay")
RE_OBS_COST = re.compile(".* costs (\d*) ore and (\d*) obsidian")


ROBOT_ORE = 0
ROBOT_CLAY = 1
ROBOT_OBSIDIAN = 2
ROBOT_GEODE = 3


class StatusQueue:
    def __init__(self):
        self.queue = []
        heapq.heapify(self.queue)

    def prioritize(self, estimate, robots, resources, rem_time):
        min_res_end = [0] * 5
        for i in range(4):
            min_res_end[i] = -1 * (resources[i] + robots[i] * rem_time)
        min_res_end[4] = -1 * estimate
        min_res_end.reverse()
        return tuple(min_res_end)

    def add(self, estimate, status):
        robots, resources, rem_time = status
        priority = self.prioritize(estimate, robots, resources, rem_time)
        heapq.heappush(self.queue, (priority, estimate, status))

    def pop(self):
        _, estimate, status = heapq.heappop(self.queue)
        return estimate, status

    def isEmpty(self):
        return len(self.queue) == 0


class GeodesSolver:

    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.max_robots_per_type = [0] * 4
        for robot in range(4):
            requirements = self._getRequirements(robot)
            for i in range(4):
                self.max_robots_per_type[i] = max(self.max_robots_per_type[i], requirements[i])

    def _getRequirements(self, construct):
        requirements = [0] * 4
        if construct == ROBOT_ORE:
            requirements[0] = self.blueprint[0][0]
        elif construct == ROBOT_CLAY:
            requirements[0] = self.blueprint[1][0]
        elif construct == ROBOT_OBSIDIAN:
            requirements[0] = self.blueprint[2][0]
            requirements[1] = self.blueprint[2][1]
        else:
            requirements[0] = self.blueprint[3][0]
            requirements[2] = self.blueprint[3][1]
        return requirements

    def estimate(self, robots, resources, rem_time):
        estimated_robots = [robot for robot in robots]
        for i in range(4):
            if estimated_robots[i] == 0:
                # Must build the robot first
                req_time = self._getRequiredTimeOptimist(estimated_robots, resources, i)
                rem_time = rem_time - 1 - req_time
                estimated_robots[i] = 1
        min_certain = resources[-1] + rem_time * estimated_robots[-1]
        # Assume we build 1 robot on each turn
        max_added = rem_time * (rem_time - 1) // 2
        return min_certain + max_added

    def _getPossibleConstructs(self, current_robots):
        if current_robots[0] < self.max_robots_per_type[0]:
            yield ROBOT_ORE
        if current_robots[1] < self.max_robots_per_type[1]:
            yield ROBOT_CLAY
        if current_robots[1] > 0 and current_robots[2] < self.max_robots_per_type[2]:
            yield ROBOT_OBSIDIAN
        if current_robots[2] > 0:
            yield ROBOT_GEODE

    def _getRequiredTimeOptimist(self, robots, resources, construct):
        """
        Return the time required to obtain the resources to build a construct.
        :param robots:
        :param resources:
        :param construct:
        :return:
        """
        requirements = self._getRequirements(construct)
        max_resource = 0
        for i, req in enumerate(requirements):
            if req > 0:
                max_resource = max(max_resource, i)
        req_time = 0
        while True:
            optimistic_build = req_time * (req_time - 1) // 2
            if requirements[max_resource] <= resources[max_resource] + robots[max_resource] * req_time + optimistic_build:
                break
            req_time += 1
        return req_time

    def _getRequiredTime(self, robots, resources, construct):
        """
        Return the time required to build the given construct.
        :param robots:
        :param resources:
        :param construct:
        :return:
        """
        requirements = self._getRequirements(construct)
        req_time = 0
        for i, required in enumerate(requirements):
            initial = resources[i]
            if initial >= required:
                continue
            res_time = int(math.ceil((required - initial) / robots[i]))
            req_time = max(res_time, req_time)
        return 1 + req_time

    def _updateResources(self, robots, resources, construct, req_time):
        new_resources = list(resources)
        consumed = self._getRequirements(construct)
        for i, robot in enumerate(robots):
            new_resources[i] += robots[i] * req_time - consumed[i]
        return tuple(new_resources)

    def solve(self, time):
        queue = StatusQueue()
        init_status = ((1, 0, 0, 0), (0, 0, 0, 0), time)
        estimate = self.estimate(*init_status)
        queue.add(estimate, init_status)
        best_result = 0
        explored = set()
        while not queue.isEmpty():
            estimate, status = queue.pop()
            if status in explored:
                continue
            explored.add(status)
            robots, resources, rem_time = status
            if estimate <= best_result:
                continue
            best_result = max(best_result, resources[-1])
            build_construct = False
            for construct in self._getPossibleConstructs(robots):
                req_time = self._getRequiredTime(robots, resources, construct)
                if req_time <= rem_time:
                    new_resources = self._updateResources(robots, resources, construct, req_time)
                    new_robots = [el for el in robots]
                    new_robots[construct] += 1
                    new_status = (tuple(new_robots), new_resources, rem_time - req_time)
                    estimate = self.estimate(*new_status)
                    queue.add(estimate, new_status)
                    build_construct = True
            if not build_construct:
                result = resources[-1] + robots[-1] * rem_time
                best_result = max(result, best_result)
        return best_result


class Solver:

    def __init__(self):
        self.blueprints = None

    def parse(self, input_file):
        self.blueprints = list()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip().split(": ")[1]
                robots_ingredients = line.split(". ")
                blueprint = [None] * 4
                cost_1 = int(RE_ORE_COST.match(robots_ingredients[0]).group(1))
                cost_2 = int(RE_ORE_COST.match(robots_ingredients[1]).group(1))
                match_3 = RE_CLAY_COST.match(robots_ingredients[2])
                cost_3 = (int(match_3.group(1)), int(match_3.group(2)))
                match_4 = RE_OBS_COST.match(robots_ingredients[3])
                cost_4 = (int(match_4.group(1)), int(match_4.group(2)))
                blueprint[0] = (cost_1, )
                blueprint[1] = (cost_2, )
                blueprint[2] = cost_3
                blueprint[3] = cost_4
                self.blueprints.append(blueprint)

    def test(self, blueprint, time):
        gsolver = GeodesSolver(blueprint)
        return gsolver.solve(time)

    def solve1(self):
        result = 0
        for i, blueprint in enumerate(self.blueprints):
            best_geodes = self.test(blueprint, 24)
            result += (i + 1) * best_geodes
        return result

    def solve2(self):
        result = 1
        for i in range(3):
            blueprint = self.blueprints[i]
            best_geodes = self.test(blueprint, 32)
            result = result * best_geodes
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
