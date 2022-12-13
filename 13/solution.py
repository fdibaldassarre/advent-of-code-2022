#!/usr/bin/env python3


class Packet:
    def __init__(self, items, is_divider=False):
        self.items = items
        self.is_divider = is_divider

    def __str__(self):
        return str(self.items)

    def __eq__(self, other):
        return self._compareItems(self.items, other.items) == 0

    def __lt__(self, other):
        return self._compareItems(self.items, other.items) < 0

    def __le__(self, other):
        return self._compareItems(self.items, other.items) <= 0

    def _compareItems(self, item_left, item_right):
        if type(item_left) != type(item_right):
            if type(item_left) == int:
                item_left = [item_left]
            else:
                item_right = [item_right]
        if type(item_left) == int and type(item_right) == int:
            if item_left == item_right:
                return 0
            return 1 if item_left > item_right else -1
        else:
            N = min(len(item_left), len(item_right))
            for i in range(N):
                res = self._compareItems(item_left[i], item_right[i])
                if res != 0:
                    return res
            if len(item_left) == len(item_right):
                return 0
            return 1 if len(item_left) > len(item_right) else -1


class Solver:

    def __init__(self):
        self.packets = None

    def parse(self, input_file):
        self.packets = list()
        with open(input_file, "r") as hand:
            other_packet = None
            for line in hand:
                line = line.strip()
                if line == "":
                    continue
                current_packet = Packet(eval(line))
                if other_packet is None:
                    other_packet = current_packet
                else:
                    self.packets.append((other_packet, current_packet))
                    other_packet = None

    def solve1(self):
        result = 0
        for i, packet in enumerate(self.packets):
            if packet[0] <= packet[1]:
                result += (i+1)
        return result

    def solve2(self):
        all_packets = list()
        all_packets.append(Packet([[2]], True))
        all_packets.append(Packet([[6]], True))
        for packet_pair in self.packets:
            all_packets.append(packet_pair[0])
            all_packets.append(packet_pair[1])
        all_packets.sort()
        result = 1
        for i, packet in enumerate(all_packets):
            if packet.is_divider:
                result *= (i+1)
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.parse("input")
    solution1 = solver.solve1()
    print("Solution 1: %d" % solution1)
    solution2 = solver.solve2()
    print("Solution 2: %d" % solution2)
