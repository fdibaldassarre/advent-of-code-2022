#!/usr/bin/env python3
import heapq
import collections


class BaseStatusQueue:
    def __init__(self, valve_to_flow):
        self.valve_to_flow = valve_to_flow
        self.heap = list()
        heapq.heapify(self.heap)
        self.valve_to_idx = dict()
        self.valves = list()
        for i, valve in enumerate(valve_to_flow.keys()):
            self.valve_to_idx[valve] = i
            self.valves.append(valve)

    def isEmpty(self):
        return len(self.heap) == 0


class StatusQueue(BaseStatusQueue):

    def _get_priority(self, valve, rem_time, current_flux, opened):
        remaining_flows = list()
        for other in self.valves:
            if other not in opened:
                flow = self.valve_to_flow[other]
                remaining_flows.append(flow)
        remaining_flows.sort(reverse=True)
        best_flow = current_flux
        for i, flow in enumerate(remaining_flows):
            dtime = rem_time - 2 * i
            if dtime <= 0:
                break
            best_flow += flow * dtime
        return -1 * best_flow

    def push(self, valve, rem_time, current_flux, opened, valve_stack):
        prio = self._get_priority(valve, rem_time, current_flux, opened)
        heapq.heappush(self.heap, (prio, valve, rem_time, current_flux, opened.copy(), valve_stack.copy()))

    def pop(self):
        (extimate, valve, rem_time, current_flux, opened, valve_stack) = heapq.heappop(self.heap)
        return -1 * extimate, valve, rem_time, current_flux, opened, valve_stack


class StatusQueueEl(BaseStatusQueue):

    def _get_priority(self, valve, rem_time, current_flux, opened):
        remaining_flows = list()
        for other in self.valves:
            if other not in opened:
                flow = self.valve_to_flow[other]
                remaining_flows.append(flow)
        remaining_flows.sort(reverse=True)
        best_flow = current_flux
        open_me = 0
        open_el = 0
        time_me = rem_time
        time_el = rem_time
        for flow in remaining_flows:
            if open_me <= open_el:
                time_me = time_me - 2 * open_me
                dtime = time_me
                open_me += 1
            else:
                time_el = time_el - 2 * open_el
                dtime = time_el
                open_el += 1
            if dtime <= 0:
                break
            best_flow += flow * dtime
        return -1 * best_flow

    def push(self, position_me, position_el, current_flux, opened, claimed, valve_stack):
        prio = self._get_priority(None, max(position_me[1], position_el[1]), current_flux, opened)
        heapq.heappush(self.heap, (prio, position_me, position_el, current_flux, opened.copy(), claimed.copy(), valve_stack.copy()))

    def pop(self):
        (extimate, position_me, position_el, current_flux, opened, claimed, valve_stack) = heapq.heappop(self.heap)
        return -1 * extimate, position_me, position_el, current_flux, opened, claimed, valve_stack

    def isEmpty(self):
        return len(self.heap) == 0


class Solver:

    def __init__(self):
        self.paths = None
        self.valves = None
        self.min_distance = None

    def parse(self, input_file):
        self.paths = dict()
        self.valves = dict()
        with open(input_file, "r") as hand:
            for line in hand:
                line = line.strip().split("; ")
                valve, flow = line[0][len("Valve "):].split(" has flow rate=")
                self.valves[valve] = int(flow)
                if "tunnels lead to valves " in line[1]:
                    connected = line[1][len("tunnels lead to valves "):].split(", ")
                else:
                    connected = line[1][len("tunnel leads to valve "):].split(", ")
                self.paths[valve] = connected
        self.min_distance = dict()
        for valve in self.valves:
            self.min_distance[valve] = self.explore(valve)

    def explore(self, start):
        explored = dict()
        explored[start] = 0
        border = collections.deque()
        border.append(start)
        while len(border) > 0:
            current = border.popleft()
            for other in self.paths[current]:
                if other not in explored:
                    explored[other] = explored[current] + 1
                    border.append(other)
        del explored[start]
        return explored

    def solve1(self):
        best_output = 0
        status_queue = StatusQueue(self.valves)
        opened = set()
        to_be_opened = 0
        for valve, flow in self.valves.items():
            if flow > 0:
                to_be_opened += 1
        status_queue.push("AA", 30, 0, opened, ["*AA"])
        while not status_queue.isEmpty():
            (extimate, valve, rem_time, current_flux, opened, valve_stack) = status_queue.pop()
            if extimate <= best_output:
                continue
            if valve not in opened and self.valves[valve] > 0 and rem_time > 1:
                opened.add(valve)
                rem_time -= 1
                current_flux = current_flux + self.valves[valve] * rem_time
                valve_stack.append(valve)
                best_output = max(best_output, current_flux)
                status_queue.push(valve, rem_time, current_flux, opened, valve_stack)
            else:
                for other, distance in self.min_distance[valve].items():
                    if other not in opened and self.valves[other] > 0:
                        status_queue.push(other, rem_time - distance, current_flux, opened, valve_stack)
        return best_output

    def solve2(self):
        best_output = 0
        status_queue = StatusQueueEl(self.valves)
        to_be_opened = 0
        for valve, flow in self.valves.items():
            if flow > 0:
                to_be_opened += 1
        possible_start = list()
        for other, distance in self.min_distance["AA"].items():
            if self.valves[other] > 0:
                possible_start.append((other, 26 - distance))
        for i, start_me in enumerate(possible_start):
            for j in range(i + 1, len(possible_start)):
                start_el = possible_start[j]
                opened = set()
                claimed = {start_me[0], start_el[0]}
                status_queue.push(start_me, start_el, 0, opened, claimed, ["*AA"])
        while not status_queue.isEmpty():
            (extimate, position_me, position_el, current_flux, opened, claimed, valve_stack) = status_queue.pop()
            if extimate <= best_output:
                continue
            move_me = True if position_me[1] >= position_el[1] else False
            valve = position_me[0] if move_me else position_el[0]
            rem_time = position_me[1] if move_me else position_el[1]
            if valve not in opened and self.valves[valve] > 0 and rem_time > 1:
                opened.add(valve)
                claimed.remove(valve)
                rem_time -= 1
                current_flux = current_flux + self.valves[valve] * rem_time
                valve_stack = valve_stack.copy()
                valve_stack.append(valve + (" (me)" if move_me else " (elephant)") + " for " + str(self.valves[valve] * rem_time))
                best_output = max(best_output, current_flux)
                if move_me:
                    position_me = (valve, rem_time)
                else:
                    position_el = (valve, rem_time)
                status_queue.push(position_me, position_el, current_flux, opened, claimed, valve_stack)
            else:
                did_move = False
                for other, distance in self.min_distance[valve].items():
                    if other not in opened and other not in claimed and self.valves[other] > 0:
                        claimed_n = claimed.copy()
                        claimed_n.add(other)
                        if move_me:
                            position_me = (other, rem_time-distance)
                        else:
                            position_el = (other, rem_time-distance)
                        did_move = True
                        status_queue.push(position_me, position_el, current_flux, opened, claimed_n, valve_stack.copy())
                if not did_move:
                    if move_me:
                        position_me = (valve, 0)
                    else:
                        position_el = (valve, 0)
                    if max(position_me[1], position_el[1]) > 0:
                        status_queue.push(position_me, position_el, current_flux, opened, claimed, valve_stack.copy())
        return best_output


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
