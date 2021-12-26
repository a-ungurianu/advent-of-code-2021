import collections
from typing import List, Tuple
from collections import defaultdict

PP = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


Pos = Tuple[int, int]


def add(a: Pos, b: Pos):
    return (a[0] + b[0], a[1] + b[1])


class Picture(object):
    def __init__(self, picture: List[str], inf_val = 0):
        self._inf_val = inf_val
        self._map = defaultdict(lambda: inf_val)
        for r, row in enumerate(picture):
            for c, val in enumerate(row):
                self._map[(r, c)] = 1 if val == "#" else 0

        self._height = len(picture)
        self._width = len(picture[0])

    def _get_value(self, pos: Pos):
        return self._map[pos]

    def _get_encoded_index(self, pos: Pos):
        index = 0
        for p in PP:
            index = (index << 1) | self._get_value(add(pos, p))
        return index

    def enrich_picture(self, algorithm: str):
        new_picture = []

        for r in range(-1, self._height + 1):
            row = ""
            for c in range(-1, self._width + 1):
                row += algorithm[self._get_encoded_index((r, c))]
            new_picture.append(row)


        if self._inf_val == 1:
            new_inf_val = 1 if algorithm[511] == "#" else 0
        else:
            new_inf_val = 1 if algorithm[0] == "#" else 0

        return Picture(new_picture, inf_val=new_inf_val)

    def __str__(self):
        res = ""
        for r in range(self._height):
            for c in range(self._width):
                res += "#" if self._map[(r, c)] == 1 else "."
            res += "\n"

        return res

    def lit_count(self):
        count = 0
        for pos in self._map.keys():
            count += self._map[pos]

        return count

with open("../input", "r") as f:
    algorithm = f.readline().strip()

    f.readline()

    picture = []
    while (line := f.readline().strip()) != "":
        picture.append(line)

    picture = Picture(picture)

for i in range(50):
    print(i + 1)
    picture = picture.enrich_picture(algorithm)
    
print(picture.lit_count())