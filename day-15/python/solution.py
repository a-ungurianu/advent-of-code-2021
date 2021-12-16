from typing import List, Tuple

from queue import PriorityQueue

DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]

Pos = Tuple[int, int]


def add(p1: Pos, p2: Pos):
    return (p1[0] + p2[0], p1[1] + p2[1])


class Map(object):
    def __init__(self, data) -> None:
        self._data = data
        self.rowCount = len(data)
        self.colCount = len(data[0])

    def _is_valid_pos(self, pos: Pos) -> bool:
        r, c = pos
        return 0 <= r < self.rowCount and 0 <= c < self.colCount

    def get_neighbours(self, pos: Pos) -> List[Pos]:
        return [add(pos, dir) for dir in DIRS if self._is_valid_pos(add(pos, dir))]

    def get_value(self, pos: Pos) -> int:
        return int(self._data[pos[0]][pos[1]])


class FiveMap(object):
    def __init__(self, map: Map) -> None:
        self.map = map

    def _is_valid_pos(self, pos: Pos) -> bool:
        r, c = pos
        return 0 <= r < self.rowCount and 0 <= c < self.colCount

    def get_value(self, pos: Pos) -> int:
        r, c = pos
        RR, rr = r // self.map.rowCount, r % self.map.rowCount
        CC, cc = c // self.map.colCount, c % self.map.colCount

        offset = RR + CC

        return ((self.map.get_value((rr, cc)) + offset) - 1) % 9 + 1

    def get_neighbours(self, pos: Pos) -> List[Pos]:
        return [add(pos, dir) for dir in DIRS if self._is_valid_pos(add(pos, dir))]

    @property
    def rowCount(self):
        return self.map.rowCount * 5

    @property
    def colCount(self):
        return self.map.colCount * 5

with open("../input") as f:
    lines = f.readlines()

map = Map([line.strip() for line in lines])


def shortest_path(map: Map, start: Pos, end: Pos):
    dist = {start: 0}

    q = PriorityQueue()
    q.put((0, start))

    while not q.empty():
        dist_to_c, c = q.get()
        if c == end:
            return dist_to_c + map.get_value(c) - map.get_value(start)

        for neigh in map.get_neighbours(c):
            dist_to_neigh = dist.get(neigh)
            if dist_to_neigh is not None and dist_to_neigh <= dist_to_c + map.get_value(
                c
            ):
                continue
            dist[neigh] = dist_to_c + map.get_value(c)
            q.put((dist[neigh], neigh))

    return None


start = (0, 0)
end = (map.rowCount - 1, map.colCount - 1)

print(shortest_path(map, start, end))

five_map = FiveMap(map)
end = (five_map.rowCount - 1, five_map.colCount - 1)
print(shortest_path(five_map, start, end))